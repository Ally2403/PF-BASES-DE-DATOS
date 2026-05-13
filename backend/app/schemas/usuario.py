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
    nombre: Optional[str] = Field(None, description="Nombre (requerido si persona nueva)")
    apellido: Optional[str] = Field(None, description="Apellido (requerido si persona nueva)")
    correo: Optional[str] = Field(None, description="Correo electrónico")
    telefono: Optional[str] = Field(None, description="Teléfono")


class UsuarioUpdate(BaseModel):
    """Datos para actualizar un usuario."""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    id_perfil: Optional[int] = Field(None)
    nombre: Optional[str] = Field(None)
    apellido: Optional[str] = Field(None)
    correo: Optional[str] = Field(None)
    telefono: Optional[str] = Field(None)


class UsuarioResponse(BaseModel):
    """Respuesta de usuario (sin contraseña)."""
    model_config = ConfigDict(populate_by_name=True)
    
    id_user: int = Field(..., validation_alias="ID_USER", description="ID único")
    username: str = Field(..., validation_alias="USERNAME", description="Usuario")
    id_perfil: int = Field(..., validation_alias="ID_PERFIL", description="ID Perfil")
    cedula: int = Field(..., validation_alias="CEDULA", description="Cédula")
    nombre: Optional[str] = Field(None, validation_alias="NOMBRE", description="Nombre")
    apellido: Optional[str] = Field(None, validation_alias="APELLIDO", description="Apellido")
    correo: Optional[str] = Field(None, validation_alias="CORREO", description="Email")
    telefono: Optional[str] = Field(None, validation_alias="TELEFONO", description="Teléfono")
    nombre_perfil: Optional[str] = Field(None, validation_alias="NOMBRE_PERFIL", description="Nombre del perfil")


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
