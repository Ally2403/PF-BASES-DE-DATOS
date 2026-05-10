"""
schemas/regla_cobro.py — Esquemas Pydantic para REGLA_COBRO
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ReglaCobroCreate(BaseModel):
    """Datos para crear regla de cobro."""
    modalidad: str = Field(..., description="GLOBAL o CREDITOS")
    id_programa: Optional[int] = Field(None, description="ID del programa (opcional, del path)")
    id_periodo: Optional[int] = Field(None, description="ID del periodo (opcional, del path)")
    valor_credito: Optional[float] = Field(None, ge=0, description="Valor por crédito (si CREDITOS)")
    valor_global: Optional[float] = Field(None, ge=0, description="Valor global (si GLOBAL)")


class ReglaCobroUpdate(BaseModel):
    """Datos para actualizar regla de cobro."""
    valor_credito: Optional[float] = Field(None, ge=0)
    valor_global: Optional[float] = Field(None, ge=0)


class ReglaCobroResponse(BaseModel):
    """Respuesta de regla de cobro."""
    model_config = ConfigDict(populate_by_name=True)
    
    modalidad: str = Field(..., validation_alias="MODALIDAD", description="GLOBAL o CREDITOS")
    valor_credito: Optional[float] = Field(None, validation_alias="VALORCREDITO", description="Valor crédito")
    valor_global: Optional[float] = Field(None, validation_alias="VALORGLOBAL", description="Valor global")
    id_programa: int = Field(..., validation_alias="ID_PROGRAMA", description="ID Programa")
    id_periodo: int = Field(..., validation_alias="ID_PERIODO", description="ID Periodo")


class ReglaCobroListResponse(BaseModel):
    """Respuesta para listar reglas."""
    success: bool = Field(...)
    message: str = Field(...)
    data: list[ReglaCobroResponse] = Field(default=[])
