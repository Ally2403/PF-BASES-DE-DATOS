"""
services/plan_estudio_asignatura.py — Lógica de negocio para PLAN_ESTUDIO_ASIGNATURA
PK compuesta: (SEMESTRE, ID_PROGRAMA, ID_ASIGNATURA)
"""

from app.services.database import execute_query, execute_update
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_asignaturas_by_plan(semestre: int, id_programa: int) -> List[Dict[str, Any]]:
    """Obtiene todas las asignaturas de un semestre en un programa."""
    try:
        query = """
            SELECT pea.SEMESTRE, pea.ID_PROGRAMA, pea.ID_ASIGNATURA, a.NOMBRE, a.CANT_CREDITOS
            FROM PLAN_ESTUDIO_ASIGNATURA pea
            JOIN ASIGNATURA a ON pea.ID_ASIGNATURA = a.ID_ASIGNATURA
            WHERE pea.SEMESTRE = :sem AND pea.ID_PROGRAMA = :id_prog
            ORDER BY pea.ID_ASIGNATURA
        """
        results = execute_query(query, {"sem": semestre, "id_prog": id_programa})
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener asignaturas: {e}")
        raise


def add_asignatura_to_plan(semestre: int, id_programa: int, id_asignatura: int) -> Dict[str, Any]:
    """Agrega una asignatura a un semestre."""
    try:
        query = """
            INSERT INTO PLAN_ESTUDIO_ASIGNATURA (SEMESTRE, ID_PROGRAMA, ID_ASIGNATURA)
            VALUES (:sem, :id_prog, :id_asig)
        """
        execute_update(query, {"sem": semestre, "id_prog": id_programa, "id_asig": id_asignatura})
        
        return {
            "SEMESTRE": semestre,
            "ID_PROGRAMA": id_programa,
            "ID_ASIGNATURA": id_asignatura
        }
    except Exception as e:
        logger.error(f"✗ Error al agregar asignatura: {e}")
        raise


def remove_asignatura_from_plan(semestre: int, id_programa: int, id_asignatura: int) -> bool:
    """Remueve una asignatura de un semestre."""
    try:
        query = """
            DELETE FROM PLAN_ESTUDIO_ASIGNATURA
            WHERE SEMESTRE = :sem AND ID_PROGRAMA = :id_prog AND ID_ASIGNATURA = :id_asig
        """
        affected = execute_update(query, {"sem": semestre, "id_prog": id_programa, "id_asig": id_asignatura})
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al remover asignatura: {e}")
        raise
