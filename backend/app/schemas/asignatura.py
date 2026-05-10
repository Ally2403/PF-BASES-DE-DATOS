"""
schemas/asignatura.py — Esquemas Pydantic para ASIGNATURA
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class AsignaturaCreate(BaseModel):
    """Datos para crear una asignatura."""
    nombre: str = Field(..., min_length=3, max_length=200, description="Nombre de la asignatura")
    cant_creditos: int = Field(..., ge=1, le=10, description="Cantidad de créditos (1-10)")


class AsignaturaUpdate(BaseModel):
    """Datos para actualizar una asignatura."""
    nombre: Optional[str] = Field(None, min_length=3, max_length=200)
    cant_creditos: Optional[int] = Field(None, ge=1, le=10)


class AsignaturaResponse(BaseModel):
    """Respuesta de asignatura."""
    model_config = ConfigDict(populate_by_name=True)
    
    id_asignatura: int = Field(..., validation_alias="ID_ASIGNATURA", description="ID único")
    nombre: str = Field(..., validation_alias="NOMBRE", description="Nombre")
    cant_creditos: int = Field(..., validation_alias="CANT_CREDITOS", description="Créditos")


class AsignaturaListResponse(BaseModel):
    """Respuesta para listar asignaturas."""
    success: bool = Field(...)
    message: str = Field(...)
    data: list[AsignaturaResponse] = Field(default=[])


class AsignaturaDetailResponse(BaseModel):
    """Respuesta para obtener/crear asignatura."""
    success: bool = Field(...)
    message: str = Field(...)
    data: Optional[AsignaturaResponse] = Field(None)
