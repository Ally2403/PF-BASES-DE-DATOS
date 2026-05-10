"""
services/auth.py — Lógica de autenticación y JWT

Maneja:
- Validación de contraseñas (SHA-256)
- Generación de tokens JWT
- Verificación de tokens
- Búsqueda de usuarios en la BD
"""

import hashlib
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from app.config import settings
from app.services.database import execute_query

logger = logging.getLogger(__name__)


# =====================================================
# UTILIDADES DE CONTRASEÑA
# =====================================================

def hash_password_sha256(password: str) -> str:
    """
    Genera el hash SHA-256 de una contraseña.
    Esto coincide con cómo Oracle almacena las contraseñas en la tabla USUARIO.
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        Hash SHA-256 en formato hexadecimal (minúsculas)
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica que la contraseña en texto plano coincida con el hash almacenado.
    
    Args:
        plain_password: Contraseña en texto plano (ingresada por el usuario)
        hashed_password: Hash SHA-256 almacenado en la BD
        
    Returns:
        True si coinciden, False si no
    """
    return hash_password_sha256(plain_password) == hashed_password.lower()


# =====================================================
# FUNCIONES DE JWT
# =====================================================

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT con los datos proporcionados.
    
    Args:
        data: Diccionario con los datos a incluir en el token
              (típicamente: {"id_user": 1, "username": "juan", "perfil": "ADMINISTRADOR"})
        expires_delta: Duración del token. Si no se proporciona, usa JWT_EXPIRATION_HOURS de config
        
    Returns:
        Token JWT codificado como string
        
    Example:
        token = create_access_token(
            {
                "id_user": 1,
                "username": "cmendoza",
                "perfil": "ADMINISTRADOR"
            }
        )
    """
    to_encode = data.copy()
    
    # Calcular tiempo de expiración
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=settings.jwt_expiration_hours)
    
    to_encode.update({"exp": expire})
    
    # Codificar JWT
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    
    logger.info(f"✓ Token JWT creado para usuario ID {data.get('id_user')}")
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verifica y decodifica un token JWT.
    
    Args:
        token: Token JWT a verificar
        
    Returns:
        Diccionario con los datos del token si es válido
        None si el token es inválido o ha expirado
        
    Example:
        payload = verify_token(token)
        if payload:
            user_id = payload.get("id_user")
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        logger.info(f"✓ Token verificado para usuario ID {payload.get('id_user')}")
        return payload
    except JWTError as e:
        logger.warning(f"✗ Token inválido o expirado: {e}")
        return None


# =====================================================
# AUTENTICACIÓN (LOGIN)
# =====================================================

def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Autentica un usuario contra la BD.
    
    Busca el usuario por username, valida la contraseña y retorna sus datos.
    
    Args:
        username: Nombre de usuario
        password: Contraseña en texto plano
        
    Returns:
        Diccionario con datos del usuario (id_user, username, perfil, etc.) si es válido
        None si el usuario no existe o contraseña es incorrecta
        
    Raises:
        Exception: Si hay error al consultar la BD
        
    Example:
        user = authenticate_user("cmendoza", "password123")
        if user:
            print(f"Bienvenido {user['username']} ({user['perfil']})")
        else:
            print("Credenciales inválidas")
    """
    try:
        # Buscar usuario en BD
        query = """
            SELECT u.ID_USER, u.USERNAME, u.CONTRASENA, u.ID_PERFIL,
                   p.NOMBRE_PERFIL, pe.CEDULA, pe.NOMBRE, pe.APELLIDO, pe.CORREO
            FROM USUARIO u
            JOIN PERFIL p ON u.ID_PERFIL = p.ID_PERFIL
            LEFT JOIN PERSONA pe ON u.CEDULA = pe.CEDULA
            WHERE LOWER(u.USERNAME) = LOWER(:username)
        """
        
        results = execute_query(query, (username,))
        
        if not results:
            logger.warning(f"✗ Usuario no encontrado: {username}")
            return None
        
        user_data = results[0]
        
        # Validar contraseña
        if not verify_password(password, user_data['CONTRASENA']):
            logger.warning(f"✗ Contraseña incorrecta para usuario: {username}")
            return None
        
        # Contraseña correcta, retornar datos del usuario
        logger.info(f"✓ Usuario autenticado exitosamente: {username}")
        return {
            "id_user": user_data['ID_USER'],
            "username": user_data['USERNAME'],
            "perfil": user_data['NOMBRE_PERFIL'],
            "cedula": user_data['CEDULA'],
            "nombre": user_data['NOMBRE'],
            "apellido": user_data['APELLIDO'],
            "correo": user_data['CORREO']
        }
        
    except Exception as e:
        logger.error(f"✗ Error al autenticar usuario: {e}")
        raise


def login_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Función wrapper para hacer login: autentica y genera token.
    
    Args:
        username: Nombre de usuario
        password: Contraseña
        
    Returns:
        Diccionario con token y datos del usuario si es exitoso
        None si fallan las credenciales
        
    Example:
        result = login_user("cmendoza", "password123")
        if result:
            token = result["access_token"]
            user = result["user"]
    """
    # Autenticar usuario
    user = authenticate_user(username, password)
    if not user:
        return None
    
    # Crear token JWT
    token_data = {
        "id_user": user["id_user"],
        "username": user["username"],
        "perfil": user["perfil"]
    }
    access_token = create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }
