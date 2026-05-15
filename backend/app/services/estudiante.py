"""
services/estudiante.py — Lógica de negocio para ESTUDIANTE
"""

from app.services.database import execute_query, execute_update
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def _generar_carnet(id_programa: int) -> str:
    """Genera un carnet único con formato AÑO-CODIGO-NNN."""
    anio = datetime.now().year
    prog = execute_query(
        "SELECT CODIGO_PROGRAMA FROM PROGRAMA_ACADEMICO WHERE ID_PROGRAMA = :id",
        {"id": id_programa}
    )
    if not prog:
        raise ValueError(f"Programa {id_programa} no encontrado")
    codigo = prog[0]['CODIGO_PROGRAMA']
    prefix = f"{anio}-{codigo}-"
    max_result = execute_query(
        """SELECT NVL(MAX(TO_NUMBER(SUBSTR(CARNET, :offset))), 0) AS MAX_SEQ
              FROM ESTUDIANTE
             WHERE ID_PROGRAMA = :id_prog
               AND CARNET LIKE :prefix_like""",
        {"offset": len(prefix) + 1, "id_prog": id_programa, "prefix_like": prefix + "%"}
    )
    seq = (max_result[0]['MAX_SEQ'] or 0) + 1
    return f"{prefix}{seq:03d}"


def get_all_estudiantes() -> List[Dict[str, Any]]:
    """Obtiene todos los estudiantes."""
    try:
        query = """
            SELECT e.ID_ESTUDIANTE, e.CARNET, e.NOMBRE, e.APELLIDO, e.TELEFONO, e.CORREO,
                   e.ID_PROGRAMA, pa.NOMBRE_PROGRAMA
            FROM ESTUDIANTE e
            LEFT JOIN PROGRAMA_ACADEMICO pa ON pa.ID_PROGRAMA = e.ID_PROGRAMA
            ORDER BY e.ID_ESTUDIANTE
        """
        results = execute_query(query)
        logger.info(f"✓ Se obtuvieron {len(results)} estudiantes")
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener estudiantes: {e}")
        raise


def get_estudiante_by_id(id_estudiante: int) -> Optional[Dict[str, Any]]:
    """Obtiene un estudiante por ID."""
    try:
        query = """
            SELECT e.ID_ESTUDIANTE, e.CARNET, e.NOMBRE, e.APELLIDO, e.TELEFONO, e.CORREO,
                   e.ID_PROGRAMA, pa.NOMBRE_PROGRAMA
            FROM ESTUDIANTE e
            LEFT JOIN PROGRAMA_ACADEMICO pa ON pa.ID_PROGRAMA = e.ID_PROGRAMA
            WHERE e.ID_ESTUDIANTE = :id
        """
        results = execute_query(query, {"id": id_estudiante})
        return results[0] if results else None
    except Exception as e:
        logger.error(f"✗ Error al obtener estudiante: {e}")
        raise


def create_estudiante(nombre: str, apellido: str, telefono: Optional[str],
                     correo: Optional[str], id_programa: int) -> Dict[str, Any]:
    """Crea un nuevo estudiante. El carnet se genera automáticamente."""
    try:
        carnet = _generar_carnet(id_programa)
        seq_result = execute_query("SELECT SEQ_ESTUDIANTE.NEXTVAL AS ID_ESTUDIANTE FROM DUAL")
        new_id = seq_result[0]['ID_ESTUDIANTE']

        query = """
            INSERT INTO ESTUDIANTE (ID_ESTUDIANTE, CARNET, NOMBRE, APELLIDO, TELEFONO, CORREO, ID_PROGRAMA)
            VALUES (:id, :carnet, :nombre, :apellido, :telefono, :correo, :id_prog)
        """
        execute_update(query, {
            "id": new_id,
            "carnet": carnet,
            "nombre": nombre,
            "apellido": apellido,
            "telefono": telefono,
            "correo": correo,
            "id_prog": id_programa
        })
        
        return get_estudiante_by_id(new_id)
    except Exception as e:
        logger.error(f"✗ Error al crear estudiante: {e}")
        raise


def update_estudiante(id_estudiante: int, nombre: str, apellido: str, telefono: Optional[str],
                     correo: Optional[str]) -> bool:
    """Actualiza un estudiante."""
    try:
        query = """
            UPDATE ESTUDIANTE
            SET NOMBRE = :nombre, APELLIDO = :apellido, TELEFONO = :telefono, CORREO = :correo
            WHERE ID_ESTUDIANTE = :id
        """
        affected = execute_update(query, {
            "id": id_estudiante,
            "nombre": nombre,
            "apellido": apellido,
            "telefono": telefono,
            "correo": correo
        })
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al actualizar estudiante: {e}")
        raise


def delete_estudiante(id_estudiante: int) -> bool:
    """Elimina un estudiante. Oracle CASCADE elimina cuenta, volantes y movimientos."""
    try:
        query = "DELETE FROM ESTUDIANTE WHERE ID_ESTUDIANTE = :id"
        affected = execute_update(query, {"id": id_estudiante})
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al eliminar estudiante: {e}")
        raise
