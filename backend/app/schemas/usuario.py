"""
schemas/usuario.py — Esquemas Pydantic para USUARIO
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class UsuarioCreate(BaseModel):
    """Datos para crear un usuario."""
    username: str = Field(..., min_length=3, max_length=50, description="Usuario único")
    contrasena: str = Field(..., min_length=6, description="Contraseña")
    id_perfil: int = Field(..., description="ID del perfil")
    cedula: int = Field(..., description="Cédula de la persona")


class UsuarioUpdate(BaseModel):
    """Datos para actualizar un usuario."""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    id_perfil: Optional[int] = Field(None)


class UsuarioResponse(BaseModel):
    """Respuesta de usuario (sin contraseña)."""
    model_config = ConfigDict(populate_by_name=True)
    
    id_user: int = Field(..., validation_alias="ID_USER", description="ID único")
    username: str = Field(..., validation_alias="USERNAME", description="Usuario")
    id_perfil: int = Field(..., validation_alias="ID_PERFIL", description="ID Perfil")
    cedula: int = Field(..., validation_alias="CEDULA", description="Cédula")


class UsuarioDetailResponse(BaseModel):
    """Respuesta para obtener/crear usuario."""
    success: bool = Field(...)
    message: str = Field(...)
    data: Optional[UsuarioResponse] = Field(None)


class UsuarioListResponse(BaseModel):
    """Respuesta para listar usuarios."""
    success: bool = Field(...)
    message: str = Field(...)
    data: list[UsuarioResponse] = Field(default=[])
