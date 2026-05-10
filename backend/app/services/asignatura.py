"""
services/asignatura.py — Lógica de negocio para ASIGNATURA
"""

from app.services.database import execute_query, execute_update
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_all_asignaturas() -> List[Dict[str, Any]]:
    """Obtiene todas las asignaturas."""
    try:
        query = "SELECT ID_ASIGNATURA, NOMBRE, CANT_CREDITOS FROM ASIGNATURA ORDER BY ID_ASIGNATURA"
        results = execute_query(query)
        logger.info(f"✓ Se obtuvieron {len(results)} asignaturas")
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener asignaturas: {e}")
        raise


def get_asignatura_by_id(id_asignatura: int) -> Optional[Dict[str, Any]]:
    """Obtiene una asignatura por ID."""
    try:
        query = "SELECT ID_ASIGNATURA, NOMBRE, CANT_CREDITOS FROM ASIGNATURA WHERE ID_ASIGNATURA = :id"
        results = execute_query(query, {"id": id_asignatura})
        return results[0] if results else None
    except Exception as e:
        logger.error(f"✗ Error al obtener asignatura: {e}")
        raise


def create_asignatura(nombre: str, cant_creditos: int) -> Dict[str, Any]:
    """Crea una nueva asignatura."""
    try:
        seq_result = execute_query("SELECT SEQ_ASIGNATURA.NEXTVAL AS ID_ASIGNATURA FROM DUAL")
        new_id = seq_result[0]['ID_ASIGNATURA']
        
        query = """
            INSERT INTO ASIGNATURA (ID_ASIGNATURA, NOMBRE, CANT_CREDITOS)
            VALUES (:id, :nombre, :creditos)
        """
        execute_update(query, {"id": new_id, "nombre": nombre, "creditos": cant_creditos})
        
        return {
            "ID_ASIGNATURA": new_id,
            "NOMBRE": nombre,
            "CANT_CREDITOS": cant_creditos
        }
    except Exception as e:
        logger.error(f"✗ Error al crear asignatura: {e}")
        raise


def update_asignatura(id_asignatura: int, nombre: str, cant_creditos: int) -> bool:
    """Actualiza una asignatura."""
    try:
        query = "UPDATE ASIGNATURA SET NOMBRE = :nombre, CANT_CREDITOS = :creditos WHERE ID_ASIGNATURA = :id"
        affected = execute_update(query, {"id": id_asignatura, "nombre": nombre, "creditos": cant_creditos})
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al actualizar asignatura: {e}")
        raise


def delete_asignatura(id_asignatura: int) -> bool:
    """Elimina una asignatura."""
    try:
        query = "DELETE FROM ASIGNATURA WHERE ID_ASIGNATURA = :id"
        affected = execute_update(query, {"id": id_asignatura})
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al eliminar asignatura: {e}")
        raise
