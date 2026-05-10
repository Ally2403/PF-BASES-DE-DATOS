"""
services/regla_cobro.py — Lógica de negocio para REGLA_COBRO
PK compuesta: (MODALIDAD, ID_PROGRAMA, ID_PERIODO)
MODALIDAD: GLOBAL o CREDITOS
"""

from app.services.database import execute_query, execute_update
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_reglas_by_programa_periodo(id_programa: int, id_periodo: int) -> List[Dict[str, Any]]:
    """Obtiene las reglas de cobro de un programa en un período."""
    try:
        query = """
            SELECT MODALIDAD, VALORCREDITO, VALORGLOBAL, ID_PROGRAMA, ID_PERIODO
            FROM REGLA_COBRO
            WHERE ID_PROGRAMA = :id_prog AND ID_PERIODO = :id_per
            ORDER BY MODALIDAD
        """
        results = execute_query(query, {"id_prog": id_programa, "id_per": id_periodo})
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener reglas: {e}")
        raise


def get_regla(modalidad: str, id_programa: int, id_periodo: int) -> Optional[Dict[str, Any]]:
    """Obtiene una regla de cobro específica."""
    try:
        query = """
            SELECT MODALIDAD, VALORCREDITO, VALORGLOBAL, ID_PROGRAMA, ID_PERIODO
            FROM REGLA_COBRO
            WHERE MODALIDAD = :mod AND ID_PROGRAMA = :id_prog AND ID_PERIODO = :id_per
        """
        results = execute_query(query, {"mod": modalidad, "id_prog": id_programa, "id_per": id_periodo})
        return results[0] if results else None
    except Exception as e:
        logger.error(f"✗ Error al obtener regla: {e}")
        raise


def create_regla(modalidad: str, id_programa: int, id_periodo: int,
                valor_credito: Optional[float] = None, valor_global: Optional[float] = None) -> Dict[str, Any]:
    """Crea una nueva regla de cobro."""
    try:
        query = """
            INSERT INTO REGLA_COBRO (MODALIDAD, ID_PROGRAMA, ID_PERIODO, VALORCREDITO, VALORGLOBAL)
            VALUES (:mod, :id_prog, :id_per, :val_cred, :val_glob)
        """
        execute_update(query, {
            "mod": modalidad,
            "id_prog": id_programa,
            "id_per": id_periodo,
            "val_cred": valor_credito,
            "val_glob": valor_global
        })
        
        return {
            "MODALIDAD": modalidad,
            "VALORCREDITO": valor_credito,
            "VALORGLOBAL": valor_global,
            "ID_PROGRAMA": id_programa,
            "ID_PERIODO": id_periodo
        }
    except Exception as e:
        logger.error(f"✗ Error al crear regla: {e}")
        raise


def update_regla(modalidad: str, id_programa: int, id_periodo: int,
                valor_credito: Optional[float] = None, valor_global: Optional[float] = None) -> bool:
    """Actualiza una regla de cobro."""
    try:
        query = """
            UPDATE REGLA_COBRO
            SET VALORCREDITO = :val_cred, VALORGLOBAL = :val_glob
            WHERE MODALIDAD = :mod AND ID_PROGRAMA = :id_prog AND ID_PERIODO = :id_per
        """
        affected = execute_update(query, {
            "mod": modalidad,
            "id_prog": id_programa,
            "id_per": id_periodo,
            "val_cred": valor_credito,
            "val_glob": valor_global
        })
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al actualizar regla: {e}")
        raise


def delete_regla(modalidad: str, id_programa: int, id_periodo: int) -> bool:
    """Elimina una regla de cobro."""
    try:
        query = """
            DELETE FROM REGLA_COBRO
            WHERE MODALIDAD = :mod AND ID_PROGRAMA = :id_prog AND ID_PERIODO = :id_per
        """
        affected = execute_update(query, {"mod": modalidad, "id_prog": id_programa, "id_per": id_periodo})
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al eliminar regla: {e}")
        raise
