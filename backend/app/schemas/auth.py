"""
schemas/auth.py — Esquemas Pydantic para autenticación

Define las estructuras de datos para:
- Solicitudes de login (username, password)
- Respuestas con tokens JWT
- Información del usuario en el token
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class LoginRequest(BaseModel):
    """
    Datos que envía el cliente para hacer login.
    
    Ejemplo:
        POST /api/auth/login
        {
            "username": "cmendoza",
            "password": "password123"
        }
    """
    username: str = Field(..., min_length=3, description="Usuario (mínimo 3 caracteres)")
    password: str = Field(..., min_length=1, description="Contraseña")


class UserInfo(BaseModel):
    """
    Información del usuario que se incluye en el token JWT.
    """
    id_user: int = Field(..., description="ID único del usuario")
    username: str = Field(..., description="Nombre de usuario")
    perfil: str = Field(..., description="Perfil: ADMINISTRADOR, SUPERVISOR, ASISTENTE")
    cedula: Optional[int] = Field(None, description="Cédula de la persona")
    nombre: Optional[str] = Field(None, description="Nombre de la persona")
    apellido: Optional[str] = Field(None, description="Apellido de la persona")
    correo: Optional[str] = Field(None, description="Correo de la persona")


class TokenResponse(BaseModel):
    """
    Respuesta del endpoint de login con el token JWT y datos del usuario.
    
    ESTRUCTURA PLANA: Todos los campos en el nivel raíz (sin anidación).
    Esto coincide con la estructura que el frontend espera en sessionStorage.
    
    Ejemplo:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "id_user": 1,
            "username": "cmendoza",
            "perfil": "ADMINISTRADOR",
            "cedula": 1001234567,
            "nombre": "Carlos",
            "apellido": "Mendoza",
            "correo": "cmendoza@example.com",
            "permisos": ["GESTIONAR_PROGRAMAS", "GESTIONAR_ESTUDIANTES", ...]
        }
    """
    access_token: str = Field(..., description="Token JWT para autenticación")
    token_type: str = Field(default="bearer", description="Tipo de token (siempre 'bearer')")
    id_user: int = Field(..., description="ID único del usuario")
    username: str = Field(..., description="Nombre de usuario")
    perfil: str = Field(..., description="Perfil: ADMINISTRADOR, SUPERVISOR, ASISTENTE")
    cedula: Optional[int] = Field(None, description="Cédula de la persona")
    nombre: Optional[str] = Field(None, description="Nombre de la persona")
    apellido: Optional[str] = Field(None, description="Apellido de la persona")
    correo: Optional[str] = Field(None, description="Correo de la persona")
    permisos: List[str] = Field(default_factory=list, description="Array de permisos del usuario")



class LoginResponse(BaseModel):
    """
    Respuesta genérica del API (envolvimiento de TokenResponse).
    """
    success: bool = Field(..., description="True si el login fue exitoso")
    message: str = Field(..., description="Mensaje descriptivo")
    data: Optional[TokenResponse] = Field(None, description="Token y datos del usuario (si success=True)")


class ErrorResponse(BaseModel):
    """
    Respuesta de error genérica.
    """
    success: bool = Field(default=False, description="Siempre False para errores")
    message: str = Field(..., description="Descripción del error")
    data: Optional[dict] = Field(None, description="Detalles adicionales del error")
