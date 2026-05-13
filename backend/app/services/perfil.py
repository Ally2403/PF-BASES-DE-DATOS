"""
services/perfil.py — Lógica de negocio para PERFIL y PERFIL_PERMISO
"""

from app.services.database import execute_query, execute_update
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_all_perfiles() -> List[Dict[str, Any]]:
    """Obtiene todos los perfiles."""
    try:
        query = "SELECT ID_PERFIL, NOMBRE_PERFIL FROM PERFIL ORDER BY ID_PERFIL"
        results = execute_query(query)
        logger.info(f"✓ Se obtuvieron {len(results)} perfiles")
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener perfiles: {e}")
        raise


def get_perfil_by_id(id_perfil: int) -> Optional[Dict[str, Any]]:
    """Obtiene un perfil por ID."""
    try:
        query = "SELECT ID_PERFIL, NOMBRE_PERFIL FROM PERFIL WHERE ID_PERFIL = :id"
        results = execute_query(query, {"id": id_perfil})
        return results[0] if results else None
    except Exception as e:
        logger.error(f"✗ Error al obtener perfil: {e}")
        raise


def get_permisos_by_perfil(id_perfil: int) -> List[int]:
    """Obtiene los IDs de permisos de un perfil."""
    try:
        query = """
            SELECT ID_PERMISO FROM PERFIL_PERMISO
            WHERE ID_PERFIL = :id_perfil
            ORDER BY ID_PERMISO
        """
        results = execute_query(query, {"id_perfil": id_perfil})
        return [r['ID_PERMISO'] for r in results]
    except Exception as e:
        logger.error(f"✗ Error al obtener permisos: {e}")
        raise


def create_perfil(nombre_perfil: str) -> Dict[str, Any]:
    """Crea un nuevo perfil."""
    try:
        # Obtener el siguiente ID
        seq_result = execute_query("SELECT SEQ_PERFIL.NEXTVAL AS ID_PERFIL FROM DUAL")
        new_id = seq_result[0]['ID_PERFIL']
        
        query = """
            INSERT INTO PERFIL (ID_PERFIL, NOMBRE_PERFIL)
            VALUES (:id, :nombre)
        """
        execute_update(query, {
            "id": new_id,
            "nombre": nombre_perfil
        })
        
        logger.info(f"✓ Perfil creado: {nombre_perfil}")
        return {
            "ID_PERFIL": new_id,
            "NOMBRE_PERFIL": nombre_perfil
        }
    except Exception as e:
        logger.error(f"✗ Error al crear perfil: {e}")
        raise


def assign_permission(id_perfil: int, id_permiso: int) -> bool:
    """Asigna un permiso a un perfil."""
    try:
        query = """
            INSERT INTO PERFIL_PERMISO (ID_PERFIL, ID_PERMISO)
            VALUES (:id_perfil, :id_permiso)
        """
        execute_update(query, {
            "id_perfil": id_perfil,
            "id_permiso": id_permiso
        })
        
        logger.info(f"✓ Permiso {id_permiso} asignado al perfil {id_perfil}")
        return True
    except Exception as e:
        logger.error(f"✗ Error al asignar permiso: {e}")
        raise


def remove_permission(id_perfil: int, id_permiso: int) -> bool:
    """Remueve un permiso de un perfil."""
    try:
        query = """
            DELETE FROM PERFIL_PERMISO
            WHERE ID_PERFIL = :id_perfil AND ID_PERMISO = :id_permiso
        """
        affected = execute_update(query, {
            "id_perfil": id_perfil,
            "id_permiso": id_permiso
        })
        
        logger.info(f"✓ Permiso {id_permiso} removido del perfil {id_perfil}")
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al remover permiso: {e}")
        raise


def get_all_permisos() -> List[Dict[str, Any]]:
    """Obtiene el catálogo completo de permisos."""
    try:
        query = """
            SELECT ID_PERMISO, NOMBRE_OPERACION, DESCRIPCION, ID_MENU
            FROM PERMISO ORDER BY ID_MENU, ID_PERMISO
        """
        results = execute_query(query)
        logger.info(f"✓ Catálogo de permisos: {len(results)} registros")
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener catálogo de permisos: {e}")
        raise


def create_permiso(nombre_operacion: str, descripcion: Optional[str], id_menu: Optional[int]) -> Dict[str, Any]:
    """Crea un nuevo permiso en el catálogo."""
    try:
        seq_result = execute_query("SELECT SEQ_PERMISO.NEXTVAL AS ID_PERMISO FROM DUAL")
        new_id = seq_result[0]['ID_PERMISO']
        execute_update(
            "INSERT INTO PERMISO (ID_PERMISO, NOMBRE_OPERACION, DESCRIPCION, ID_MENU) VALUES (:id, :nom, :desc, :id_menu)",
            {"id": new_id, "nom": nombre_operacion, "desc": descripcion, "id_menu": id_menu}
        )
        logger.info(f"✓ Permiso creado: {nombre_operacion}")
        return {"ID_PERMISO": new_id, "NOMBRE_OPERACION": nombre_operacion, "DESCRIPCION": descripcion, "ID_MENU": id_menu}
    except Exception as e:
        logger.error(f"✗ Error al crear permiso: {e}")
        raise


def delete_permiso(id_permiso: int) -> bool:
    """Elimina un permiso del catálogo (cascade elimina PERFIL_PERMISO)."""
    try:
        affected = execute_update("DELETE FROM PERMISO WHERE ID_PERMISO = :id", {"id": id_permiso})
        logger.info(f"✓ Permiso {id_permiso} eliminado")
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al eliminar permiso: {e}")
        raise
