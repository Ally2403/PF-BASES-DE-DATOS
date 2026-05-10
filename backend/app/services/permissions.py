"""
services/permissions.py — Sistema de control de permisos por perfil

Proporciona decoradores FastAPI para proteger endpoints según el perfil del usuario:
- ADMINISTRADOR (acceso total)
- SUPERVISOR (datos base)
- ASISTENTE (cobros)
"""

from fastapi import Depends, HTTPException, status, Header
from jose import JWTError
from app.services.auth import verify_token
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


def extract_token_from_header(authorization: Optional[str] = None) -> Optional[str]:
    """
    Extrae el token JWT del header Authorization: Bearer <token>
    
    Args:
        authorization: Header Authorization (ej: "Bearer eyJhbGc...")
        
    Returns:
        Token JWT sin "Bearer " o None si no existe
    """
    if not authorization:
        return None
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    
    return parts[1]


def require_perfil(perfiles_permitidos: List[str]):
    """
    Decorador FastAPI que valida que el usuario esté autenticado
    y pertenezca a uno de los perfiles permitidos.
    
    Uso:
        @router.get("/api/programas")
        async def listar_programas(current_user: dict = Depends(require_perfil(["SUPERVISOR", "ADMINISTRADOR"]))):
            # Solo SUPERVISOR o ADMINISTRADOR pueden acceder
            return {...}
    
    Args:
        perfiles_permitidos: Lista de perfiles permitidos (ej: ["SUPERVISOR", "ADMINISTRADOR"])
        
    Returns:
        Función dependencia que retorna los datos del usuario si tiene permiso
        
    Raises:
        HTTPException (401): Si no está autenticado
        HTTPException (403): Si no tiene el perfil requerido
    """
    async def verify_user(authorization: Optional[str] = Header(None)) -> dict:
        """Verifica el token y el perfil del usuario"""
        
        # Extraer token
        token = extract_token_from_header(authorization)
        if not token:
            logger.warning("✗ No se proporcionó token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No autorizado. Proporciona token en header Authorization: Bearer <token>"
            )
        
        # Verificar token
        payload = verify_token(token)
        if not payload:
            logger.warning("✗ Token inválido o expirado")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado"
            )
        
        # Verificar perfil
        perfil_usuario = payload.get("perfil")
        if perfil_usuario not in perfiles_permitidos:
            logger.warning(f"✗ Usuario {payload.get('username')} con perfil {perfil_usuario} intenta acceder a recurso protegido")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Perfiles requeridos: {', '.join(perfiles_permitidos)}"
            )
        
        logger.info(f"✓ Acceso permitido para usuario {payload.get('username')} ({perfil_usuario})")
        return payload
    
    return verify_user


def require_any_auth(authorization: Optional[str] = Header(None)) -> dict:
    """
    Dependencia que solo valida autenticación (cualquier usuario autenticado).
    
    Uso:
        @router.get("/api/mi-perfil")
        async def mi_perfil(current_user: dict = Depends(require_any_auth)):
            return current_user
    
    Args:
        authorization: Header Authorization
        
    Returns:
        Datos del usuario si está autenticado
        
    Raises:
        HTTPException (401): Si no está autenticado o token es inválido
    """
    token = extract_token_from_header(authorization)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autorizado"
        )
    
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    return payload
