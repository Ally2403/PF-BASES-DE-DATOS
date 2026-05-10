"""
services/plan_estudio.py — Lógica de negocio para PLAN_ESTUDIO
PK compuesta: (SEMESTRE, ID_PROGRAMA)
"""

from app.services.database import execute_query, execute_update
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_all_planes() -> List[Dict[str, Any]]:
    """Obtiene todos los planes de estudio."""
    try:
        query = "SELECT SEMESTRE, ID_PROGRAMA FROM PLAN_ESTUDIO ORDER BY ID_PROGRAMA, SEMESTRE"
        results = execute_query(query)
        logger.info(f"✓ Se obtuvieron {len(results)} planes")
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener planes: {e}")
        raise


def get_planes_by_programa(id_programa: int) -> List[Dict[str, Any]]:
    """Obtiene todos los semestres de un programa."""
    try:
        query = "SELECT SEMESTRE, ID_PROGRAMA FROM PLAN_ESTUDIO WHERE ID_PROGRAMA = :id_prog ORDER BY SEMESTRE"
        results = execute_query(query, {"id_prog": id_programa})
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener planes del programa: {e}")
        raise


def create_plan(semestre: int, id_programa: int) -> Dict[str, Any]:
    """Crea un nuevo semestre en un plan de estudio."""
    try:
        query = """
            INSERT INTO PLAN_ESTUDIO (SEMESTRE, ID_PROGRAMA)
            VALUES (:semestre, :id_prog)
        """
        execute_update(query, {"semestre": semestre, "id_prog": id_programa})
        
        return {
            "SEMESTRE": semestre,
            "ID_PROGRAMA": id_programa
        }
    except Exception as e:
        logger.error(f"✗ Error al crear plan: {e}")
        raise


def delete_plan(semestre: int, id_programa: int) -> bool:
    """Elimina un semestre de un plan de estudio."""
    try:
        query = "DELETE FROM PLAN_ESTUDIO WHERE SEMESTRE = :sem AND ID_PROGRAMA = :id_prog"
        affected = execute_update(query, {"sem": semestre, "id_prog": id_programa})
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al eliminar plan: {e}")
        raise
