"""
schemas/periodo.py — Esquemas Pydantic para PERIODO_ACADEMICO
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional


class PeriodoCreate(BaseModel):
    """Datos para crear un periodo académico."""
    nombre_periodo: str = Field(..., min_length=2, max_length=20, description="Nombre del periodo (ej: '2024-I')")
    fecha_inicio: date = Field(..., description="Fecha de inicio (YYYY-MM-DD)")
    fecha_fin: date = Field(..., description="Fecha de fin (YYYY-MM-DD)")


class PeriodoUpdate(BaseModel):
    """Datos para actualizar un periodo académico."""
    nombre_periodo: Optional[str] = Field(None, min_length=2, max_length=20)
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None


class PeriodoResponse(BaseModel):
    """Respuesta de periodo académico."""
    model_config = ConfigDict(populate_by_name=True)
    
    id_periodo: int = Field(..., validation_alias="ID_PERIODO", description="ID único")
    nombre_periodo: str = Field(..., validation_alias="NOMBRE_PERIODO", description="Nombre del periodo")
    fecha_inicio: date = Field(..., validation_alias="FECHA_INICIO", description="Fecha inicio")
    fecha_fin: date = Field(..., validation_alias="FECHA_FIN", description="Fecha fin")


class PeriodoListResponse(BaseModel):
    """Respuesta genérica para listar periodos."""
    success: bool = Field(..., description="Éxito de operación")
    message: str = Field(..., description="Mensaje descriptivo")
    data: list[PeriodoResponse] = Field(default=[], description="Lista de periodos")


class PeriodoDetailResponse(BaseModel):
    """Respuesta genérica para obtener/crear un periodo."""
    success: bool = Field(...)
    message: str = Field(...)
    data: Optional[PeriodoResponse] = Field(None)
