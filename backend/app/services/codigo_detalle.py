"""
services/codigo_detalle.py — Lógica de negocio para CODIGO_DETALLE
"""

from app.services.database import execute_query, execute_update
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_all_codigos() -> List[Dict[str, Any]]:
    """Obtiene todos los códigos de detalle."""
    try:
        query = "SELECT CODIGO_DETALLE, GRUPO, DESCRIPCION, VALOR_DEFECTO FROM CODIGO_DETALLE ORDER BY CODIGO_DETALLE"
        results = execute_query(query)
        logger.info(f"✓ Se obtuvieron {len(results)} códigos")
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener códigos: {e}")
        raise


def get_codigo_by_id(codigo: str) -> Optional[Dict[str, Any]]:
    """Obtiene un código por código (es la PK)."""
    try:
        query = "SELECT CODIGO_DETALLE, GRUPO, DESCRIPCION, VALOR_DEFECTO FROM CODIGO_DETALLE WHERE CODIGO_DETALLE = :codigo"
        results = execute_query(query, {"codigo": codigo})
        return results[0] if results else None
    except Exception as e:
        logger.error(f"✗ Error al obtener código: {e}")
        raise


def create_codigo(codigo_detalle: str, grupo: str, descripcion: str, valor_defecto: Optional[float] = None) -> Dict[str, Any]:
    """Crea un nuevo código de detalle."""
    try:
        query = """
            INSERT INTO CODIGO_DETALLE (CODIGO_DETALLE, GRUPO, DESCRIPCION, VALOR_DEFECTO)
            VALUES (:codigo, :grupo, :descripcion_param, :valor_param)
        """
        execute_update(query, {"codigo": codigo_detalle, "grupo": grupo, "descripcion_param": descripcion, "valor_param": valor_defecto})
        
        return {
            "CODIGO_DETALLE": codigo_detalle,
            "GRUPO": grupo,
            "DESCRIPCION": descripcion,
            "VALOR_DEFECTO": valor_defecto
        }
    except Exception as e:
        logger.error(f"✗ Error al crear código: {e}")
        raise


def update_codigo(codigo_detalle: str, descripcion: str, valor_defecto: Optional[float] = None) -> bool:
    """Actualiza un código de detalle."""
    try:
        query = "UPDATE CODIGO_DETALLE SET DESCRIPCION = :descripcion_param, VALOR_DEFECTO = :valor_param WHERE CODIGO_DETALLE = :codigo"
        affected = execute_update(query, {"codigo": codigo_detalle, "descripcion_param": descripcion, "valor_param": valor_defecto})
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al actualizar código: {e}")
        raise


def delete_codigo(codigo_detalle: str) -> bool:
    """Elimina un código de detalle."""
    try:
        query = "DELETE FROM CODIGO_DETALLE WHERE CODIGO_DETALLE = :codigo"
        affected = execute_update(query, {"codigo": codigo_detalle})
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al eliminar código: {e}")
        raise
