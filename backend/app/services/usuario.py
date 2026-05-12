"""
services/usuario.py — Lógica de negocio para USUARIO
"""

from app.services.database import execute_query, execute_update
from app.services.auth import hash_password_sha256
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_all_usuarios() -> List[Dict[str, Any]]:
    """Obtiene todos los usuarios."""
    try:
        query = """
            SELECT u.ID_USER, u.USERNAME, u.ID_PERFIL, u.CEDULA,
                   p.NOMBRE, p.APELLIDO, p.CORREO, p.TELEFONO,
                   pf.NOMBRE_PERFIL
            FROM USUARIO u
            LEFT JOIN PERSONA p  ON p.CEDULA     = u.CEDULA
            LEFT JOIN PERFIL  pf ON pf.ID_PERFIL = u.ID_PERFIL
            ORDER BY u.ID_USER
        """
        results = execute_query(query)
        logger.info(f"✓ Se obtuvieron {len(results)} usuarios")
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener usuarios: {e}")
        raise


def get_usuario_by_id(id_user: int) -> Optional[Dict[str, Any]]:
    """Obtiene un usuario por ID."""
    try:
        query = """
            SELECT u.ID_USER, u.USERNAME, u.ID_PERFIL, u.CEDULA,
                   p.NOMBRE, p.APELLIDO, p.CORREO, p.TELEFONO,
                   pf.NOMBRE_PERFIL
            FROM USUARIO u
            LEFT JOIN PERSONA p  ON p.CEDULA     = u.CEDULA
            LEFT JOIN PERFIL  pf ON pf.ID_PERFIL = u.ID_PERFIL
            WHERE u.ID_USER = :id
        """
        results = execute_query(query, {"id": id_user})
        return results[0] if results else None
    except Exception as e:
        logger.error(f"✗ Error al obtener usuario: {e}")
        raise


def get_usuario_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Obtiene un usuario por username."""
    try:
        query = """
            SELECT u.ID_USER, u.USERNAME, u.ID_PERFIL, u.CEDULA,
                   p.NOMBRE, p.APELLIDO, p.CORREO, p.TELEFONO,
                   pf.NOMBRE_PERFIL
            FROM USUARIO u
            LEFT JOIN PERSONA p  ON p.CEDULA     = u.CEDULA
            LEFT JOIN PERFIL  pf ON pf.ID_PERFIL = u.ID_PERFIL
            WHERE u.USERNAME = :user
        """
        results = execute_query(query, {"user": username})
        return results[0] if results else None
    except Exception as e:
        logger.error(f"✗ Error al obtener usuario por username: {e}")
        raise


def create_usuario(username: str, contrasena: str, id_perfil: int, cedula: int) -> Dict[str, Any]:
    """Crea un nuevo usuario."""
    try:
        # Obtener el siguiente ID
        seq_result = execute_query("SELECT SEQ_USUARIO.NEXTVAL AS ID_USER FROM DUAL")
        new_id = seq_result[0]['ID_USER']
        
        # Hash de la contraseña
        password_hash = hash_password_sha256(contrasena)
        
        query = """
            INSERT INTO USUARIO (ID_USER, USERNAME, CONTRASENA, ID_PERFIL, CEDULA)
            VALUES (:id, :username, :contrasena, :id_perfil, :cedula)
        """
        execute_update(query, {
            "id": new_id,
            "username": username,
            "contrasena": password_hash,
            "id_perfil": id_perfil,
            "cedula": cedula
        })
        
        logger.info(f"✓ Usuario creado: {username}")
        return get_usuario_by_id(new_id)
    except Exception as e:
        logger.error(f"✗ Error al crear usuario: {e}")
        raise


def update_usuario(id_user: int, username: Optional[str] = None, id_perfil: Optional[int] = None) -> bool:
    """Actualiza un usuario."""
    try:
        # Obtener datos actuales
        usuario = get_usuario_by_id(id_user)
        if not usuario:
            return False
        
        # Usar valores nuevos o mantener los actuales
        nuevo_username = username if username else usuario['USERNAME']
        nuevo_id_perfil = id_perfil if id_perfil else usuario['ID_PERFIL']
        
        query = """
            UPDATE USUARIO
            SET USERNAME = :username, ID_PERFIL = :id_perfil
            WHERE ID_USER = :id
        """
        affected = execute_update(query, {
            "id": id_user,
            "username": nuevo_username,
            "id_perfil": nuevo_id_perfil
        })
        
        logger.info(f"✓ Usuario actualizado: {id_user}")
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al actualizar usuario: {e}")
        raise


def delete_usuario(id_user: int) -> bool:
    """Elimina un usuario."""
    try:
        query = "DELETE FROM USUARIO WHERE ID_USER = :id"
        affected = execute_update(query, {"id": id_user})
        logger.info(f"✓ Usuario eliminado: {id_user}")
        return affected > 0
    except Exception as e:
        logger.error(f"✗ Error al eliminar usuario: {e}")
        raise
