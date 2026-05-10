"""
schemas/perfil.py — Esquemas Pydantic para PERFIL y PERFIL_PERMISO
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class PerfilCreate(BaseModel):
    """Datos para crear un perfil."""
    nombre_perfil: str = Field(..., min_length=1, max_length=50, description="Nombre del perfil")


class PerfilResponse(BaseModel):
    """Respuesta de perfil."""
    model_config = ConfigDict(populate_by_name=True)
    
    id_perfil: int = Field(..., validation_alias="ID_PERFIL", description="ID único")
    nombre_perfil: str = Field(..., validation_alias="NOMBRE_PERFIL", description="Nombre")


class PermisoResponse(BaseModel):
    """Respuesta de permiso."""
    model_config = ConfigDict(populate_by_name=True)
    
    id_permiso: int = Field(..., validation_alias="ID_PERMISO", description="ID")
    id_perfil: int = Field(..., validation_alias="ID_PERFIL", description="ID Perfil")


class PerfilConPermisosResponse(BaseModel):
    """Respuesta de perfil con sus permisos."""
    model_config = ConfigDict(populate_by_name=True)
    
    id_perfil: int = Field(..., validation_alias="ID_PERFIL", description="ID único")
    nombre_perfil: str = Field(..., validation_alias="NOMBRE_PERFIL", description="Nombre")
    permisos: list[int] = Field(default=[], description="IDs de permisos")


class PerfilListResponse(BaseModel):
    """Respuesta para listar perfiles."""
    success: bool = Field(...)
    message: str = Field(...)
    data: list[PerfilConPermisosResponse] = Field(default=[])


class PerfilDetailResponse(BaseModel):
    """Respuesta para obtener/crear perfil."""
    success: bool = Field(...)
    message: str = Field(...)
    data: Optional[PerfilResponse] = Field(None)
