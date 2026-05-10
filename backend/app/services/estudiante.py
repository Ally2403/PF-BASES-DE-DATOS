"""
services/estudiante.py — Lógica de negocio para ESTUDIANTE
"""

from app.services.database import execute_query, execute_update
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_all_estudiantes() -> List[Dict[str, Any]]:
    """Obtiene todos los estudiantes."""
    try:
        query = """
            SELECT ID_ESTUDIANTE, CARNET, NOMBRE, APELLIDO, TELEFONO, CORREO, ID_PROGRAMA
            FROM ESTUDIANTE ORDER BY ID_ESTUDIANTE
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
            SELECT ID_ESTUDIANTE, CARNET, NOMBRE, APELLIDO, TELEFONO, CORREO, ID_PROGRAMA
            FROM ESTUDIANTE WHERE ID_ESTUDIANTE = :id
        """
        results = execute_query(query, {"id": id_estudiante})
        return results[0] if results else None
    except Exception as e:
        logger.error(f"✗ Error al obtener estudiante: {e}")
        raise


def create_estudiante(carnet: Optional[str], nombre: str, apellido: str, telefono: Optional[str],
                     correo: Optional[str], id_programa: int) -> Dict[str, Any]:
    """Crea un nuevo estudiante."""
    try:
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
        
        return {
            "ID_ESTUDIANTE": new_id,
            "CARNET": carnet,
            "NOMBRE": nombre,
            "APELLIDO": apellido,
            "TELEFONO": telefono,
            "CORREO": correo,
            "ID_PROGRAMA": id_programa
        }
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
    """Elimina un estudiante."""
    try:
        query = "DELETE FROM ESTUDIANTE WHERE ID_ESTUDIANTE = :id"
        affected = execute_update(query, {"id": id_estudiante})
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al eliminar estudiante: {e}")
        raise
