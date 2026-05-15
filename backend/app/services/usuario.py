"""
services/usuario.py — Lógica de negocio para USUARIO
"""

from app.services.database import execute_query, execute_update
from app.services.auth import hash_password_sha256
from app.services.persona import get_persona_by_cedula, create_persona, update_persona
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


def create_usuario(username: str, contrasena: str, id_perfil: int, cedula: int,
                   nombre: Optional[str] = None, apellido: Optional[str] = None,
                   correo: Optional[str] = None, telefono: Optional[str] = None) -> Dict[str, Any]:
    """Crea un nuevo usuario, creando o actualizando la persona asociada si es necesario."""
    try:
        # 1. Verificar si ya existe la PERSONA con esa cédula
        persona = get_persona_by_cedula(cedula)
        if not persona:
            # Persona nueva: nombre, apellido y correo son obligatorios
            if not nombre or not apellido or not correo:
                raise ValueError(
                    "Para registrar un usuario con una cédula nueva debe proporcionar "
                    "nombre, apellido y correo electrónico."
                )
            create_persona(cedula, nombre, apellido, correo, telefono)
        else:
            # Persona ya existe: actualizar sólo los campos que se envíen
            if any(v is not None for v in [nombre, apellido, correo, telefono]):
                update_persona(cedula, nombre, apellido, correo, telefono)

        # 2. Obtener el siguiente ID de secuencia
        seq_result = execute_query("SELECT SEQ_USUARIO.NEXTVAL AS ID_USER FROM DUAL")
        new_id = seq_result[0]['ID_USER']

        # 3. Hash de la contraseña
        password_hash = hash_password_sha256(contrasena)

        # 4. Insertar USUARIO
        insert_query = """
            INSERT INTO USUARIO (ID_USER, USERNAME, CONTRASENA, ID_PERFIL, CEDULA)
            VALUES (:id, :username, :contrasena, :id_perfil, :cedula)
        """
        execute_update(insert_query, {
            "id": new_id,
            "username": username,
            "contrasena": password_hash,
            "id_perfil": id_perfil,
            "cedula": cedula
        })

        logger.info(f"✓ Usuario creado: {username}")
        return get_usuario_by_id(new_id)
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"✗ Error al crear usuario: {e}")
        raise


def update_usuario(id_user: int, username: Optional[str] = None, id_perfil: Optional[int] = None,
                   nombre: Optional[str] = None, apellido: Optional[str] = None,
                   correo: Optional[str] = None, telefono: Optional[str] = None) -> bool:
    """Actualiza un usuario y su persona asociada."""
    try:
        usuario = get_usuario_by_id(id_user)
        if not usuario:
            return False

        nuevo_username = username if username else usuario['USERNAME']
        nuevo_id_perfil = id_perfil if id_perfil else usuario['ID_PERFIL']

        # 1. Actualizar USUARIO
        execute_update(
            "UPDATE USUARIO SET USERNAME = :username, ID_PERFIL = :id_perfil WHERE ID_USER = :id",
            {"id": id_user, "username": nuevo_username, "id_perfil": nuevo_id_perfil}
        )

        # 2. Actualizar PERSONA si se proporcionó al menos un campo
        if any(v is not None for v in [nombre, apellido, correo, telefono]):
            execute_update(
                """UPDATE PERSONA
                   SET NOMBRE   = COALESCE(:nombre,   NOMBRE),
                       APELLIDO = COALESCE(:apellido, APELLIDO),
                       CORREO   = COALESCE(:correo,   CORREO),
                       TELEFONO = COALESCE(:telefono, TELEFONO)
                   WHERE CEDULA = (SELECT CEDULA FROM USUARIO WHERE ID_USER = :id)""",
                {"id": id_user, "nombre": nombre, "apellido": apellido,
                 "correo": correo, "telefono": telefono}
            )

        logger.info(f"✓ Usuario actualizado: {id_user}")
        return True
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


def reset_and_email_contrasena(id_user: int) -> str:
    """Genera una nueva contraseña temporal, la guarda en la BD y envía un correo al usuario.
    Retorna el correo al que se envió."""
    from app.services.email_service import generar_contrasena_temporal, enviar_credenciales

    usuario = get_usuario_by_id(id_user)
    if not usuario:
        raise ValueError(f"Usuario {id_user} no encontrado")

    correo = usuario.get('CORREO')
    if not correo:
        raise ValueError("El usuario no tiene correo electrónico registrado")

    nueva_contrasena = generar_contrasena_temporal()
    nuevo_hash = hash_password_sha256(nueva_contrasena)

    execute_update(
        "UPDATE USUARIO SET CONTRASENA = :pw WHERE ID_USER = :id",
        {"pw": nuevo_hash, "id": id_user}
    )
    logger.info(f"✓ Contraseña reseteada para usuario {id_user}")

    nombre_completo = f"{usuario.get('NOMBRE', '')} {usuario.get('APELLIDO', '')}".strip()
    enviar_credenciales(correo, nombre_completo, usuario['USERNAME'], nueva_contrasena)

    return correo
