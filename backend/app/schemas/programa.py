"""
schemas/programa.py — Esquemas Pydantic para PROGRAMA_ACADEMICO
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ProgramaCreate(BaseModel):
    """
    Datos para crear un nuevo programa académico.
    
    Ejemplo:
        {
            "nombre_programa": "Ingeniería en Sistemas"
        }
    """
    nombre_programa: str = Field(..., min_length=3, max_length=100, description="Nombre del programa")


class ProgramaUpdate(BaseModel):
    """
    Datos para actualizar un programa académico.
    """
    nombre_programa: Optional[str] = Field(None, min_length=3, max_length=100)


class ProgramaResponse(BaseModel):
    """
    Respuesta al listar o crear un programa.
    
    Ejemplo:
        {
            "id_programa": 1,
            "nombre_programa": "Ingeniería en Sistemas"
        }
    """
    model_config = ConfigDict(populate_by_name=True)
    
    id_programa: int = Field(..., validation_alias="ID_PROGRAMA", description="ID único del programa")
    nombre_programa: str = Field(..., validation_alias="NOMBRE_PROGRAMA", description="Nombre del programa")


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
