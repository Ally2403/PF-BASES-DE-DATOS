"""
schemas/movimiento.py — Esquemas Pydantic para MOVIMIENTO y TRANSACCION_PAGO
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date, datetime


class MovimientoCreate(BaseModel):
    """Datos para crear un movimiento (cobro o pago)."""
    codigo_detalle: str = Field(..., max_length=10, description="Código de detalle (PMAT, PCRE, PCAR, PLAB, PEXA, MPAG, etc)")
    valor: float = Field(..., gt=0, description="Valor del movimiento")
    id_volante: Optional[int] = Field(None, description="ID del volante (opcional para cobros adicionales)")
    id_periodo: int = Field(..., description="ID del período")


class CobroAdicionalCreate(BaseModel):
    """Datos para crear un cobro adicional sobre un volante existente."""
    id_volante: int = Field(..., description="ID del volante existente")
    codigo_detalle: str = Field(..., max_length=10, description="PCAR, PLAB, PEXA, etc")
    valor: float = Field(..., gt=0, description="Valor del cobro adicional")


class PagoCreate(BaseModel):
    """Datos para registrar un pago."""
    id_volante: int = Field(..., description="ID del volante a pagar")
    medio_pago: str = Field(..., max_length=30, description="Efectivo, Transferencia, Tarjeta, etc")
    valor: float = Field(..., gt=0, description="Valor pagado")
    referencia: Optional[str] = Field(None, max_length=100, description="Referencia del pago (ej: número de comprobante)")


class MovimientoResponse(BaseModel):
    """Respuesta de movimiento."""
    model_config = ConfigDict(populate_by_name=True)
    
    id_mov: int = Field(..., validation_alias="ID_MOV", description="ID único")
    fecha: datetime = Field(..., validation_alias="FECHA", description="Fecha")
    valor: float = Field(..., validation_alias="VALOR", description="Valor")
    codigo_detalle: str = Field(..., validation_alias="CODIGO_DETALLE", description="Código")
    id_volante: Optional[int] = Field(None, validation_alias="ID_VOLANTE", description="ID Volante")
    id_periodo: int = Field(..., validation_alias="ID_PERIODO", description="ID Período")


class TransaccionPagoResponse(BaseModel):
    """Respuesta de transacción de pago."""
    model_config = ConfigDict(populate_by_name=True)
    
    id_transaccion: int = Field(..., validation_alias="ID_TRANSACCION", description="ID único")
    id_mov: int = Field(..., validation_alias="ID_MOV", description="ID Movimiento")
    medio_pago: str = Field(..., validation_alias="MEDIO_PAGO", description="Medio de pago")
    referencia: Optional[str] = Field(None, validation_alias="REFERENCIA", description="Referencia")
    fecha_pago: datetime = Field(..., validation_alias="FECHA_PAGO", description="Fecha pago")


class MovimientoListResponse(BaseModel):
    """Respuesta para listar movimientos."""
    success: bool = Field(...)
    message: str = Field(...)
    data: list[MovimientoResponse] = Field(default=[])


class PagoDetailResponse(BaseModel):
    """Respuesta para crear pago."""
    success: bool = Field(...)
    message: str = Field(...)
    data: Optional[TransaccionPagoResponse] = Field(None)
