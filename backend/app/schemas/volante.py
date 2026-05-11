"""
schemas/volante.py — Esquemas Pydantic para VOLANTE_MATRICULA
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime


class VolanteCreate(BaseModel):
    """Datos para crear un volante individual o masivo."""
    id_estudiante: Optional[int] = Field(None, description="ID del estudiante (para individual)")
    id_periodo: int = Field(..., description="ID del período académico")
    id_programa: int = Field(..., description="ID del programa")
    modalidad: str = Field(..., description="GLOBAL o CREDITOS")
    semestre_que_cobra: int = Field(..., ge=1, le=10, description="Semestre a cobrar (1-10)")
    tipo_generacion: str = Field(default="INDIVIDUAL", description="INDIVIDUAL o MASIVA")


class VolanteResponse(BaseModel):
    """Respuesta de volante."""
    model_config = ConfigDict(populate_by_name=True)
    
    id_volante: int = Field(..., validation_alias="ID_VOLANTE", description="ID único")
    estado: str = Field(..., validation_alias="ESTADO", description="PENDIENTE, PARCIAL, PAGADO")
    monto_total: float = Field(..., validation_alias="MONTO_TOTAL", description="Monto total")
    id_estudiante: int = Field(..., validation_alias="ID_ESTUDIANTE", description="ID Estudiante")
    id_periodo: int = Field(..., validation_alias="ID_PERIODO", description="ID Período")
    id_programa: int = Field(..., validation_alias="ID_PROGRAMA", description="ID Programa")
    modalidad: str = Field(..., validation_alias="MODALIDAD", description="Modalidad")
    semestre_que_cobra: int = Field(..., validation_alias="SEMESTRE_QUE_COBRA", description="Semestre")
    fecha_generacion: datetime = Field(..., validation_alias="FECHA_GENERACION", description="Fecha")
    tipo_generacion: str = Field(..., validation_alias="TIPO_GENERACION", description="Tipo generación")


class VolanteListResponse(BaseModel):
    """Respuesta para listar volantes."""
    success: bool = Field(...)
    message: str = Field(...)
    data: list[VolanteResponse] = Field(default=[])


class VolanteDetailResponse(BaseModel):
    """Respuesta para obtener/crear volante."""
    success: bool = Field(...)
    message: str = Field(...)
    data: Optional[VolanteResponse] = Field(None)
