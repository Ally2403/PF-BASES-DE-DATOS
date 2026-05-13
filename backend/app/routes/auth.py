"""
routes/auth.py — Endpoints de autenticación

Expone:
- POST /api/auth/login → Autentica usuario y retorna JWT
"""

from fastapi import APIRouter, HTTPException, status, Header
from app.schemas.auth import LoginRequest, TokenResponse, LoginResponse, ErrorResponse
from app.services.auth import login_user, verify_token
from app.services.permissions import extract_token_from_header
from app.services.database import execute_query
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Crear router para autenticación
router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Login de usuario",
    description="Autentica un usuario con username y password, retorna JWT token"
)
async def login(credentials: LoginRequest) -> LoginResponse:
    """
    Endpoint para hacer login.
    
    **Flujo:**
    1. Recibe username y password
    2. Busca usuario en tabla USUARIO
    3. Valida contraseña (SHA-256)
    4. Genera token JWT
    5. Retorna token + información del usuario
    
    **Ejemplo de uso:**
    ```bash
    curl -X POST http://localhost:8000/api/auth/login \
      -H "Content-Type: application/json" \
      -d '{"username": "cmendoza", "password": "password123"}'
    ```
    
    **Respuesta exitosa (200):**
    ```json
    {
        "success": true,
        "message": "Login exitoso",
        "data": {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "user": {
                "id_user": 1,
                "username": "cmendoza",
                "perfil": "ADMINISTRADOR",
                "cedula": 1001234567,
                "nombre": "Carlos",
                "apellido": "Mendoza",
                "correo": "cmendoza@example.com"
            }
        }
    }
    ```
    
    **Respuesta fallo (401):**
    ```json
    {
        "success": false,
        "message": "Credenciales inválidas",
        "data": null
    }
    ```
    
    Args:
        credentials: Objeto LoginRequest con username y password
        
    Returns:
        LoginResponse con token y datos del usuario
        
    Raises:
        HTTPException (401): Si credenciales son inválidas
    """
    try:
        # Intentar login
        result = login_user(credentials.username, credentials.password)
        
        if not result:
            logger.warning(f"✗ Login fallido para usuario: {credentials.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas"
            )
        
        # Login exitoso
        logger.info(f"✓ Login exitoso para usuario: {credentials.username}")
        
        return LoginResponse(
            success=True,
            message="Login exitoso",
            data=TokenResponse(
                access_token=result["access_token"],
                token_type=result["token_type"],
                id_user=result["id_user"],
                username=result["username"],
                perfil=result["perfil"],
                cedula=result.get("cedula"),
                nombre=result.get("nombre"),
                apellido=result.get("apellido"),
                correo=result.get("correo"),
                permisos=result.get("permisos", [])
            )
        )
        
    except HTTPException:
        # Re-raise errores HTTP
        raise
    except Exception as e:
        logger.error(f"✗ Error en endpoint login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/me", summary="Obtener permisos actuales del usuario autenticado")
async def get_me(authorization: Optional[str] = Header(None)):
    """
    Retorna los permisos frescos desde la BD para el usuario del token.
    Útil para refrescar permisos sin hacer re-login.
    """
    token = extract_token_from_header(authorization)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado")

    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

    try:
        results = execute_query(
            """SELECT DISTINCT pm.NOMBRE_OPERACION
               FROM USUARIO u
               JOIN PERFIL_PERMISO pp ON pp.ID_PERFIL = u.ID_PERFIL
               JOIN PERMISO pm ON pp.ID_PERMISO = pm.ID_PERMISO
               WHERE u.ID_USER = :id_user
               ORDER BY pm.NOMBRE_OPERACION""",
            {"id_user": payload["id_user"]}
        )
        permisos = [r["NOMBRE_OPERACION"] for r in results]
        return {"success": True, "permisos": permisos}
    except Exception as e:
        logger.error(f"✗ Error en /me: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
