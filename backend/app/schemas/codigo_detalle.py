"""
schemas/codigo_detalle.py — Esquemas Pydantic para CODIGO_DETALLE
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CodigoDetalleCreate(BaseModel):
    """Datos para crear código de detalle."""
    codigo_detalle: str = Field(..., min_length=1, max_length=10, description="Código (ej: PLAB, PEXA)")
    grupo: str = Field(..., description="Grupo: COBRO o PAGO")
    descripcion: str = Field(..., min_length=3, max_length=200, description="Descripción")
    valor_defecto: Optional[float] = Field(None, ge=0, description="Valor por defecto")


class CodigoDetalleUpdate(BaseModel):
    """Datos para actualizar código de detalle."""
    descripcion: Optional[str] = Field(None, min_length=3, max_length=200)
    valor_defecto: Optional[float] = Field(None, ge=0)


class CodigoDetalleResponse(BaseModel):
    """Respuesta de código de detalle."""
    model_config = ConfigDict(populate_by_name=True)
    
    codigo_detalle: str = Field(..., validation_alias="CODIGO_DETALLE", description="Código")
    grupo: str = Field(..., validation_alias="GRUPO", description="COBRO o PAGO")
    descripcion: str = Field(..., validation_alias="DESCRIPCION", description="Descripción")
    valor_defecto: Optional[float] = Field(None, validation_alias="VALOR_DEFECTO", description="Valor")
    tiene_movimientos: Optional[bool] = Field(None, validation_alias="TIENE_MOVIMIENTOS", description="Tiene movimientos registrados")


class CodigoDetalleListResponse(BaseModel):
    """Respuesta para listar códigos."""
    success: bool = Field(...)
    message: str = Field(...)
    data: list[CodigoDetalleResponse] = Field(default=[])


class CodigoDetalleDetailResponse(BaseModel):
    """Respuesta para obtener/crear código."""
    success: bool = Field(...)
    message: str = Field(...)
    data: Optional[CodigoDetalleResponse] = Field(None)
