"""
schemas/plan_estudio.py — Esquemas Pydantic para PLAN_ESTUDIO
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class PlanEstudioCreate(BaseModel):
    """Datos para crear semestre en plan de estudio."""
    semestre: int = Field(..., ge=1, le=10, description="Semestre (1-10)")
    id_programa: Optional[int] = Field(None, description="ID del programa (opcional, se obtiene del path)")


class PlanEstudioResponse(BaseModel):
    """Respuesta de plan de estudio."""
    model_config = ConfigDict(populate_by_name=True)
    
    semestre: int = Field(..., validation_alias="SEMESTRE", description="Semestre")
    id_programa: int = Field(..., validation_alias="ID_PROGRAMA", description="ID Programa")


class PlanEstudioListResponse(BaseModel):
    """Respuesta para listar planes."""
    success: bool = Field(...)
    message: str = Field(...)
    data: list[PlanEstudioResponse] = Field(default=[])
