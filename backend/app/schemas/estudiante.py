"""
schemas/estudiante.py — Esquemas Pydantic para ESTUDIANTE
"""

from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional


class EstudianteCreate(BaseModel):
    """Datos para crear un estudiante. El carnet se genera automáticamente."""
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[str] = Field(None, max_length=150)
    id_programa: int = Field(..., description="ID del programa académico")


class EstudianteUpdate(BaseModel):
    """Datos para actualizar un estudiante."""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(None, min_length=1, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    correo: Optional[str] = Field(None, max_length=150)


class EstudianteResponse(BaseModel):
    """Respuesta de estudiante."""
    model_config = ConfigDict(populate_by_name=True)
    
    id_estudiante: int = Field(..., validation_alias="ID_ESTUDIANTE", description="ID único")
    carnet: Optional[str] = Field(None, validation_alias="CARNET", description="Carnet")
    nombre: str = Field(..., validation_alias="NOMBRE", description="Nombre")
    apellido: str = Field(..., validation_alias="APELLIDO", description="Apellido")
    telefono: Optional[str] = Field(None, validation_alias="TELEFONO", description="Teléfono")
    correo: Optional[str] = Field(None, validation_alias="CORREO", description="Email")
    id_programa: int = Field(..., validation_alias="ID_PROGRAMA", description="ID Programa")
    nombre_programa: Optional[str] = Field(None, validation_alias="NOMBRE_PROGRAMA", description="Nombre del programa")


class EstudianteListResponse(BaseModel):
    """Respuesta para listar estudiantes."""
    success: bool = Field(...)
    message: str = Field(...)
    data: list[EstudianteResponse] = Field(default=[])


class EstudianteDetailResponse(BaseModel):
    """Respuesta para obtener/crear estudiante."""
    success: bool = Field(...)
    message: str = Field(...)
    data: Optional[EstudianteResponse] = Field(None)
