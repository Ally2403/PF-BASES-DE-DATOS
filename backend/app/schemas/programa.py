"""
schemas/programa.py — Esquemas Pydantic para PROGRAMA_ACADEMICO
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ProgramaCreate(BaseModel):
    nombre_programa: str = Field(..., min_length=3, max_length=200, description="Nombre del programa")
    codigo_programa: str = Field(..., min_length=2, max_length=10, description="Sigla del programa (ej. SIS, ADM)")


class ProgramaUpdate(BaseModel):
    nombre_programa: Optional[str] = Field(None, min_length=3, max_length=200)
    codigo_programa: Optional[str] = Field(None, min_length=2, max_length=10)


class ProgramaResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id_programa: int = Field(..., validation_alias="ID_PROGRAMA")
    nombre_programa: str = Field(..., validation_alias="NOMBRE_PROGRAMA")
    codigo_programa: str = Field(..., validation_alias="CODIGO_PROGRAMA")


class ProgramaListResponse(BaseModel):
    """
    Respuesta genérica para listar programas.
    """
    success: bool = Field(..., description="True si la operación fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo")
    data: list[ProgramaResponse] = Field(default=[], description="Lista de programas")


class ProgramaDetailResponse(BaseModel):
    """
    Respuesta genérica para obtener/crear un programa.
    """
    success: bool = Field(..., description="True si la operación fue exitosa")
    message: str = Field(..., description="Mensaje descriptivo")
    data: Optional[ProgramaResponse] = Field(None, description="Datos del programa")
