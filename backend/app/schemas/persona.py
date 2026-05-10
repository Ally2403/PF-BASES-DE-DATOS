"""
schemas/persona.py — Esquemas Pydantic para PERSONA
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class PersonaCreate(BaseModel):
    """Datos para crear una persona."""
    cedula: int = Field(..., description="Número de cédula (único)")
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre")
    apellido: str = Field(..., min_length=1, max_length=100, description="Apellido")
    correo: str = Field(..., max_length=150, description="Email (único)")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono")


class PersonaResponse(BaseModel):
    """Respuesta de persona."""
    model_config = ConfigDict(populate_by_name=True)
    
    cedula: int = Field(..., validation_alias="CEDULA", description="Cédula")
    nombre: str = Field(..., validation_alias="NOMBRE", description="Nombre")
    apellido: str = Field(..., validation_alias="APELLIDO", description="Apellido")
    correo: str = Field(..., validation_alias="CORREO", description="Email")
    telefono: Optional[str] = Field(None, validation_alias="TELEFONO", description="Teléfono")


class PersonaListResponse(BaseModel):
    """Respuesta para listar personas."""
    success: bool = Field(...)
    message: str = Field(...)
    data: list[PersonaResponse] = Field(default=[])


class PersonaDetailResponse(BaseModel):
    """Respuesta para obtener/crear persona."""
    success: bool = Field(...)
    message: str = Field(...)
    data: Optional[PersonaResponse] = Field(None)
