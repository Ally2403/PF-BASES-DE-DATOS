"""
services/persona.py — Lógica de negocio para PERSONA
"""

from app.services.database import execute_query, execute_update
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_all_personas() -> List[Dict[str, Any]]:
    """Obtiene todas las personas."""
    try:
        query = "SELECT CEDULA, NOMBRE, APELLIDO, CORREO, TELEFONO FROM PERSONA ORDER BY CEDULA"
        results = execute_query(query)
        logger.info(f"✓ Se obtuvieron {len(results)} personas")
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener personas: {e}")
        raise


def get_persona_by_cedula(cedula: int) -> Optional[Dict[str, Any]]:
    """Obtiene una persona por cédula."""
    try:
        query = "SELECT CEDULA, NOMBRE, APELLIDO, CORREO, TELEFONO FROM PERSONA WHERE CEDULA = :ced"
        results = execute_query(query, {"ced": cedula})
        return results[0] if results else None
    except Exception as e:
        logger.error(f"✗ Error al obtener persona: {e}")
        raise


def create_persona(cedula: int, nombre: str, apellido: str, correo: str, telefono: Optional[str]) -> Dict[str, Any]:
    """Crea una nueva persona."""
    try:
        query = """
            INSERT INTO PERSONA (CEDULA, NOMBRE, APELLIDO, CORREO, TELEFONO)
            VALUES (:ced, :nombre, :apellido, :correo, :telefono)
        """
        execute_update(query, {
            "ced": cedula,
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "telefono": telefono
        })
        
        logger.info(f"✓ Persona creada: {cedula}")
        return {
            "CEDULA": cedula,
            "NOMBRE": nombre,
            "APELLIDO": apellido,
            "CORREO": correo,
            "TELEFONO": telefono
        }
    except Exception as e:
        logger.error(f"✗ Error al crear persona: {e}")
        raise


def delete_persona(cedula: int) -> bool:
    """Elimina una persona. Por FK ON DELETE CASCADE, también elimina el usuario asociado."""
    try:
        query = "DELETE FROM PERSONA WHERE CEDULA = :ced"
        affected = execute_update(query, {"ced": cedula})
        if affected > 0:
            logger.info(f"✓ Persona {cedula} eliminada (cascade elimina usuario asociado)")
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al eliminar persona: {e}")
        raise


def update_persona(cedula: int, nombre: Optional[str] = None, apellido: Optional[str] = None,
                   correo: Optional[str] = None, telefono: Optional[str] = None) -> bool:
    """Actualiza una persona."""
    try:
        # Obtener datos actuales
        persona = get_persona_by_cedula(cedula)
        if not persona:
            return False
        
        # Usar valores nuevos o mantener los actuales
        nuevo_nombre = nombre if nombre else persona['NOMBRE']
        nuevo_apellido = apellido if apellido else persona['APELLIDO']
        nuevo_correo = correo if correo else persona['CORREO']
        nuevo_telefono = telefono if telefono is not None else persona.get('TELEFONO')
        
        query = """
            UPDATE PERSONA
            SET NOMBRE = :nombre, APELLIDO = :apellido, CORREO = :correo, TELEFONO = :telefono
            WHERE CEDULA = :ced
        """
        affected = execute_update(query, {
            "ced": cedula,
            "nombre": nuevo_nombre,
            "apellido": nuevo_apellido,
            "correo": nuevo_correo,
            "telefono": nuevo_telefono
        })
        
        logger.info(f"✓ Persona actualizada: {cedula}")
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al actualizar persona: {e}")
        raise
