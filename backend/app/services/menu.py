"""
services/menu.py — Lógica de negocio para MENU
"""

from app.services.database import execute_query, execute_update
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_all_menus() -> List[Dict[str, Any]]:
    """Obtiene todos los menús."""
    try:
        query = "SELECT ID_MENU, NOMBRE_FUNCION, URL_ACCESO FROM MENU ORDER BY ID_MENU"
        results = execute_query(query)
        logger.info(f"✓ Se obtuvieron {len(results)} menús")
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener menús: {e}")
        raise


def get_menu_by_id(id_menu: int) -> Optional[Dict[str, Any]]:
    """Obtiene un menú por ID."""
    try:
        query = "SELECT ID_MENU, NOMBRE_FUNCION, URL_ACCESO FROM MENU WHERE ID_MENU = :id"
        results = execute_query(query, {"id": id_menu})
        return results[0] if results else None
    except Exception as e:
        logger.error(f"✗ Error al obtener menú: {e}")
        raise


def create_menu(nombre_funcion: str, url_acceso: Optional[str] = None) -> Dict[str, Any]:
    """Crea un nuevo menú."""
    try:
        # Obtener el siguiente ID
        seq_result = execute_query("SELECT SEQ_MENU.NEXTVAL AS ID_MENU FROM DUAL")
        new_id = seq_result[0]['ID_MENU']
        
        query = """
            INSERT INTO MENU (ID_MENU, NOMBRE_FUNCION, URL_ACCESO)
            VALUES (:id, :nombre, :url)
        """
        execute_update(query, {
            "id": new_id,
            "nombre": nombre_funcion,
            "url": url_acceso
        })
        
        logger.info(f"✓ Menú creado: {nombre_funcion}")
        return {
            "ID_MENU": new_id,
            "NOMBRE_FUNCION": nombre_funcion,
            "URL_ACCESO": url_acceso
        }
    except Exception as e:
        logger.error(f"✗ Error al crear menú: {e}")
        raise


def update_menu(id_menu: int, nombre_funcion: Optional[str] = None, url_acceso: Optional[str] = None) -> bool:
    """Actualiza un menú."""
    try:
        # Obtener datos actuales
        menu = get_menu_by_id(id_menu)
        if not menu:
            return False
        
        # Usar valores nuevos o mantener los actuales
        nuevo_nombre = nombre_funcion if nombre_funcion else menu['NOMBRE_FUNCION']
        nuevo_url = url_acceso if url_acceso is not None else menu.get('URL_ACCESO')
        
        query = """
            UPDATE MENU
            SET NOMBRE_FUNCION = :nombre, URL_ACCESO = :url
            WHERE ID_MENU = :id
        """
        affected = execute_update(query, {
            "id": id_menu,
            "nombre": nuevo_nombre,
            "url": nuevo_url
        })
        
        logger.info(f"✓ Menú actualizado: {id_menu}")
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al actualizar menú: {e}")
        raise


def delete_menu(id_menu: int) -> bool:
    """Elimina un menú."""
    try:
        query = "DELETE FROM MENU WHERE ID_MENU = :id"
        affected = execute_update(query, {"id": id_menu})
        logger.info(f"✓ Menú eliminado: {id_menu}")
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al eliminar menú: {e}")
        raise
