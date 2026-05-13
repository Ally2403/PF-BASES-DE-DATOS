"""
services/movimiento.py — Lógica de negocio para MOVIMIENTO y TRANSACCION_PAGO
"""

from app.services.database import execute_query, execute_update
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def get_movimientos_by_volante(id_volante: int) -> List[Dict[str, Any]]:
    """Obtiene todos los movimientos de un volante."""
    try:
        query = """
            SELECT ID_MOV, FECHA, VALOR, CODIGO_DETALLE, ID_VOLANTE, ID_PERIODO, ID_CUENTA
            FROM MOVIMIENTO WHERE ID_VOLANTE = :id_vol
            ORDER BY FECHA DESC
        """
        results = execute_query(query, {"id_vol": id_volante})
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener movimientos: {e}")
        raise


def get_movimiento_by_id(id_mov: int) -> Optional[Dict[str, Any]]:
    """Obtiene un movimiento específico."""
    try:
        query = """
            SELECT ID_MOV, FECHA, VALOR, CODIGO_DETALLE, ID_VOLANTE, ID_PERIODO, ID_CUENTA
            FROM MOVIMIENTO WHERE ID_MOV = :id
        """
        results = execute_query(query, {"id": id_mov})
        return results[0] if results else None
    except Exception as e:
        logger.error(f"✗ Error al obtener movimiento: {e}")
        raise


def get_cuenta_by_estudiante(id_estudiante: int) -> Optional[int]:
    """Obtiene el ID de la CUENTA_CORRIENTE de un estudiante.
    La cuenta es creada automáticamente por el trigger TR_CREAR_CUENTA_CORRIENTE.
    Nota: CUENTA_CORRIENTE es UNIQUE por estudiante (no por periodo)."""
    try:
        query = """
            SELECT ID_CUENTA FROM CUENTA_CORRIENTE 
            WHERE ID_ESTUDIANTE = :id_est
        """
        results = execute_query(query, {"id_est": id_estudiante})
        return results[0]['ID_CUENTA'] if results else None
    except Exception as e:
        logger.error(f"✗ Error al obtener cuenta: {e}")
        raise


def _ensure_cuenta_corriente(id_estudiante: int) -> int:
    """Obtiene o crea la CUENTA_CORRIENTE del estudiante."""
    id_cuenta = get_cuenta_by_estudiante(id_estudiante)
    if not id_cuenta:
        seq = execute_query("SELECT SEQ_CUENTA.NEXTVAL AS ID_CUENTA FROM DUAL")
        id_cuenta = seq[0]['ID_CUENTA']
        execute_update(
            "INSERT INTO CUENTA_CORRIENTE (ID_CUENTA, ID_ESTUDIANTE) VALUES (:id, :est)",
            {"id": id_cuenta, "est": id_estudiante}
        )
        logger.info(f"✓ CC auto-creada para estudiante {id_estudiante}: id={id_cuenta}")
    return id_cuenta


def crear_cobro_adicional(id_volante: Optional[int], codigo_detalle: str, valor: float,
                          id_estudiante: Optional[int] = None, id_periodo: Optional[int] = None) -> Dict[str, Any]:
    """Crea un movimiento de cobro adicional (PCAR, PLAB, PEXA, etc).
    Si hay volante, se obtiene estudiante/periodo desde él.
    Si no hay volante, se requiere id_estudiante + id_periodo directamente.
    La CC se crea automáticamente si no existe."""
    try:
        # Resolver volante → estudiante/periodo
        if id_volante is not None:
            volante = execute_query(
                "SELECT ID_ESTUDIANTE, ID_PERIODO FROM VOLANTE_MATRICULA WHERE ID_VOLANTE = :id",
                {"id": id_volante}
            )
            if not volante:
                raise ValueError(f"Volante {id_volante} no encontrado")
            id_estudiante = volante[0]['ID_ESTUDIANTE']
            id_periodo = volante[0]['ID_PERIODO']
        else:
            # Sin volante: se requiere estudiante + periodo
            if not id_estudiante or not id_periodo:
                raise ValueError("Debe proporcionar id_volante o (id_estudiante + id_periodo)")
            # Buscar si existe volante para asociar (opcional, no obligatorio)
            vol_lookup = execute_query(
                "SELECT ID_VOLANTE FROM VOLANTE_MATRICULA WHERE ID_ESTUDIANTE = :est AND ID_PERIODO = :per",
                {"est": id_estudiante, "per": id_periodo}
            )
            if vol_lookup:
                id_volante = vol_lookup[0]['ID_VOLANTE']
            # Si no hay volante, id_volante queda None → MOVIMIENTO.ID_VOLANTE es nullable

        # Auto-crear CC si no existe
        id_cuenta = _ensure_cuenta_corriente(id_estudiante)

        # Insertar movimiento
        seq_result = execute_query("SELECT SEQ_MOVIMIENTO.NEXTVAL AS ID_MOV FROM DUAL")
        new_id = seq_result[0]['ID_MOV']

        execute_update(
            """INSERT INTO MOVIMIENTO (ID_MOV, FECHA, VALOR, CODIGO_DETALLE, ID_VOLANTE, ID_PERIODO, ID_CUENTA)
               VALUES (:id, SYSDATE, :valor, :cod_det, :id_vol, :id_per, :id_cuenta)""",
            {
                "id": new_id,
                "valor": valor,
                "cod_det": codigo_detalle,
                "id_vol": id_volante,
                "id_per": id_periodo,
                "id_cuenta": id_cuenta
            }
        )

        logger.info(f"✓ Cobro adicional creado: {codigo_detalle} x {valor}, volante={id_volante}, est={id_estudiante}")
        return get_movimiento_by_id(new_id)
    except Exception as e:
        logger.error(f"✗ Error al crear cobro: {e}")
        raise


def registrar_pago(id_volante: int, medio_pago: str, valor: float, referencia: Optional[str] = None, codigo_detalle: str = 'MPAG') -> Dict[str, Any]:
    """Registra un pago: inserta en MOVIMIENTO y luego en TRANSACCION_PAGO.
    El trigger TR_ACTUALIZAR_ESTADO_VOLANTE actualizará el estado."""
    try:
        # Obtener datos del volante
        volante = execute_query(
            "SELECT ID_ESTUDIANTE, ID_PERIODO FROM VOLANTE_MATRICULA WHERE ID_VOLANTE = :id",
            {"id": id_volante}
        )
        
        if not volante:
            raise ValueError(f"Volante {id_volante} no encontrado")
        
        id_estudiante = volante[0]['ID_ESTUDIANTE']
        id_periodo = volante[0]['ID_PERIODO']
        
        # Obtener la cuenta
        id_cuenta = get_cuenta_by_estudiante(id_estudiante)
        if not id_cuenta:
            raise ValueError(f"Cuenta corriente no existe")
        
        # Obtener ID de movimiento
        seq_mov = execute_query("SELECT SEQ_MOVIMIENTO.NEXTVAL AS ID_MOV FROM DUAL")
        id_mov = seq_mov[0]['ID_MOV']
        
        # Insertar en MOVIMIENTO con el código de pago recibido
        query_mov = """
            INSERT INTO MOVIMIENTO (ID_MOV, FECHA, VALOR, CODIGO_DETALLE, ID_VOLANTE, ID_PERIODO, ID_CUENTA)
            VALUES (:id, SYSDATE, :valor, :cod_det, :id_vol, :id_per, :id_cuenta)
        """
        execute_update(query_mov, {
            "id": id_mov,
            "valor": valor,
            "cod_det": codigo_detalle,
            "id_vol": id_volante,
            "id_per": id_periodo,
            "id_cuenta": id_cuenta
        })
        
        # Obtener ID de transacción
        seq_trans = execute_query("SELECT SEQ_TRANSACCION.NEXTVAL AS ID_TRANSACCION FROM DUAL")
        id_trans = seq_trans[0]['ID_TRANSACCION']
        
        # Insertar en TRANSACCION_PAGO
        query_pago = """
            INSERT INTO TRANSACCION_PAGO (ID_TRANSACCION, ID_MOV, MEDIO_PAGO, REFERENCIA, FECHA_PAGO)
            VALUES (:id_trans, :id_mov, :medio, :ref, SYSDATE)
        """
        execute_update(query_pago, {
            "id_trans": id_trans,
            "id_mov": id_mov,
            "medio": medio_pago,
            "ref": referencia
        })
        
        logger.info(f"✓ Pago registrado: ${valor} para volante {id_volante} via {medio_pago}")
        
        # Retornar la transacción
        return execute_query(
            "SELECT ID_TRANSACCION, ID_MOV, MEDIO_PAGO, REFERENCIA, FECHA_PAGO FROM TRANSACCION_PAGO WHERE ID_TRANSACCION = :id",
            {"id": id_trans}
        )[0]
    except Exception as e:
        logger.error(f"✗ Error al registrar pago: {e}")
        raise


def eliminar_movimiento(id_mov: int) -> bool:
    """Elimina un movimiento. Si es el principal (PMAT, PCRE), el trigger 
    TR_BORRAR_VOLANTE_POR_MOVIMIENTO eliminará el volante automáticamente.
    También elimina la TRANSACCION_PAGO asociada si existe (FK sin CASCADE)."""
    try:
        # Primero eliminar TRANSACCION_PAGO asociada (FK sin CASCADE)
        execute_update(
            "DELETE FROM TRANSACCION_PAGO WHERE ID_MOV = :id",
            {"id": id_mov}
        )
        
        # Luego eliminar el movimiento
        query = "DELETE FROM MOVIMIENTO WHERE ID_MOV = :id"
        affected = execute_update(query, {"id": id_mov})
        
        if affected > 0:
            logger.info(f"✓ Movimiento {id_mov} eliminado")
        
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al eliminar movimiento: {e}")
        raise
