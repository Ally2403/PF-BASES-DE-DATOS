"""
schemas/plan_estudio_asignatura.py — Esquemas Pydantic para PLAN_ESTUDIO_ASIGNATURA
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class PlanEstudioAsignaturaCreate(BaseModel):
    """Datos para agregar asignatura a un semestre."""
    semestre: Optional[int] = Field(None, ge=1, le=10, description="Semestre (opcional, del path)")
    id_programa: Optional[int] = Field(None, description="ID del programa (opcional, del path)")
    id_asignatura: int = Field(..., description="ID de la asignatura")


class PlanEstudioAsignaturaResponse(BaseModel):
    """Respuesta de plan estudio asignatura."""
    model_config = ConfigDict(populate_by_name=True)
    
    semestre: int = Field(..., validation_alias="SEMESTRE", description="Semestre")
    id_programa: int = Field(..., validation_alias="ID_PROGRAMA", description="ID Programa")
    id_asignatura: int = Field(..., validation_alias="ID_ASIGNATURA", description="ID Asignatura")
    nombre: Optional[str] = Field(None, validation_alias="NOMBRE", description="Nombre asignatura")
    cant_creditos: Optional[int] = Field(None, validation_alias="CANT_CREDITOS", description="Créditos")


class PlanEstudioAsignaturaListResponse(BaseModel):
    """Respuesta para listar asignaturas de un plan."""
    success: bool = Field(...)
    message: str = Field(...)
    data: list[PlanEstudioAsignaturaResponse] = Field(default=[])
