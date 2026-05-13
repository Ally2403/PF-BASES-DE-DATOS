"""
schemas/menu.py — Esquemas Pydantic para MENU y PERMISO
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List


class MenuCreate(BaseModel):
    """Datos para crear un menú."""
    nombre_funcion: str = Field(..., min_length=1, max_length=100, description="Nombre de la función")
    url_acceso: Optional[str] = Field(None, max_length=200, description="URL de acceso")


class MenuResponse(BaseModel):
    """Respuesta de menú."""
    model_config = ConfigDict(populate_by_name=True)
    
    id_menu: int = Field(..., validation_alias="ID_MENU", description="ID único")
    nombre_funcion: str = Field(..., validation_alias="NOMBRE_FUNCION", description="Nombre de función")
    url_acceso: Optional[str] = Field(None, validation_alias="URL_ACCESO", description="URL de acceso")


class MenuListResponse(BaseModel):
    """Respuesta para listar menús."""
    success: bool = Field(...)
    message: str = Field(...)
    data: List[MenuResponse] = Field(default=[])


class MenuDetailResponse(BaseModel):
    """Respuesta para obtener/crear menú."""
    success: bool = Field(...)
    message: str = Field(...)
    data: Optional[MenuResponse] = Field(None)


# ---- PERMISO ----

class PermisoCreate(BaseModel):
    """Datos para crear un permiso."""
    nombre_operacion: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=300)
    id_menu: Optional[int] = Field(None)


class PermisoResponse(BaseModel):
    """Respuesta de permiso del catálogo."""
    model_config = ConfigDict(populate_by_name=True)

    id_permiso: int = Field(..., validation_alias="ID_PERMISO")
    nombre_operacion: str = Field(..., validation_alias="NOMBRE_OPERACION")
    descripcion: Optional[str] = Field(None, validation_alias="DESCRIPCION")
    id_menu: Optional[int] = Field(None, validation_alias="ID_MENU")


class PermisoListResponse(BaseModel):
    """Respuesta para listar permisos."""
    success: bool = Field(...)
    message: str = Field(...)
    data: List[PermisoResponse] = Field(default=[])

