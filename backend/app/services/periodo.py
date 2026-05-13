"""
services/periodo.py — Lógica de negocio para PERIODO_ACADEMICO
"""

from app.services.database import execute_query, execute_update
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_all_periodos() -> List[Dict[str, Any]]:
    """Obtiene todos los períodos académicos."""
    try:
        query = "SELECT ID_PERIODO, NOMBRE_PERIODO, FECHA_INICIO, FECHA_FIN FROM PERIODO_ACADEMICO ORDER BY ID_PERIODO"
        results = execute_query(query)
        logger.info(f"✓ Se obtuvieron {len(results)} períodos")
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener períodos: {e}")
        raise


def get_periodo_by_id(id_periodo: int) -> Optional[Dict[str, Any]]:
    """Obtiene un período por ID."""
    try:
        query = "SELECT ID_PERIODO, NOMBRE_PERIODO, FECHA_INICIO, FECHA_FIN FROM PERIODO_ACADEMICO WHERE ID_PERIODO = :id"
        results = execute_query(query, {"id": id_periodo})
        return results[0] if results else None
    except Exception as e:
        logger.error(f"✗ Error al obtener período: {e}")
        raise


def create_periodo(nombre_periodo: str, fecha_inicio: str, fecha_fin: str) -> Dict[str, Any]:
    """Crea un nuevo período académico."""
    try:
        from datetime import datetime
        
        seq_result = execute_query("SELECT SEQ_PERIODO.NEXTVAL AS ID_PERIODO FROM DUAL")
        new_id = seq_result[0]['ID_PERIODO']
        
        query = """
            INSERT INTO PERIODO_ACADEMICO (ID_PERIODO, NOMBRE_PERIODO, FECHA_INICIO, FECHA_FIN)
            VALUES (:id, :nombre, TO_DATE(:inicio, 'YYYY-MM-DD'), TO_DATE(:fin, 'YYYY-MM-DD'))
        """
        execute_update(query, {"id": new_id, "nombre": nombre_periodo, "inicio": fecha_inicio, "fin": fecha_fin})
        
        # Convertir strings a objetos date para Pydantic
        inicio_date = datetime.strptime(fecha_inicio, '%Y-%m-%d').date() if isinstance(fecha_inicio, str) else fecha_inicio
        fin_date = datetime.strptime(fecha_fin, '%Y-%m-%d').date() if isinstance(fecha_fin, str) else fecha_fin
        
        return {
            "ID_PERIODO": new_id,
            "NOMBRE_PERIODO": nombre_periodo,
            "FECHA_INICIO": inicio_date,
            "FECHA_FIN": fin_date
        }
    except Exception as e:
        logger.error(f"✗ Error al crear período: {e}")
        raise


def update_periodo(id_periodo: int, nombre_periodo: str, fecha_inicio: str, fecha_fin: str) -> bool:
    """Actualiza un período académico."""
    try:
        query = """
            UPDATE PERIODO_ACADEMICO 
            SET NOMBRE_PERIODO = :nombre, FECHA_INICIO = TO_DATE(:inicio, 'YYYY-MM-DD'), FECHA_FIN = TO_DATE(:fin, 'YYYY-MM-DD')
            WHERE ID_PERIODO = :id
        """
        affected = execute_update(query, {"id": id_periodo, "nombre": nombre_periodo, "inicio": fecha_inicio, "fin": fecha_fin})
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al actualizar período: {e}")
        raise


def delete_periodo(id_periodo: int) -> bool:
    """Elimina un período académico. Oracle CASCADE elimina REGLA_COBRO, VOLANTE_MATRICULA
    y MOVIMIENTO asociados al período."""
    try:
        query = "DELETE FROM PERIODO_ACADEMICO WHERE ID_PERIODO = :id"
        affected = execute_update(query, {"id": id_periodo})
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al eliminar período: {e}")
        raise
