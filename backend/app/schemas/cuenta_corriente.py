"""
schemas/cuenta_corriente.py — Esquemas Pydantic para CUENTA_CORRIENTE y vistas
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date


class CuentaCorrienteDetalleResponse(BaseModel):
    """Respuesta de detalle de cuenta corriente (VW_CUENTA_CORRIENTE_DETALLE)."""
    model_config = ConfigDict(populate_by_name=True)

    id_estudiante: int = Field(..., validation_alias="ID_ESTUDIANTE")
    carnet: Optional[str] = Field(None, validation_alias="CARNET")
    nombre_completo: str = Field(..., validation_alias="NOMBRE_COMPLETO")
    nombre_programa: str = Field(..., validation_alias="NOMBRE_PROGRAMA")
    nombre_periodo: str = Field(..., validation_alias="NOMBRE_PERIODO")
    id_mov: int = Field(..., validation_alias="ID_MOV")
    fecha: date = Field(..., validation_alias="FECHA")
    codigo_detalle: str = Field(..., validation_alias="CODIGO_DETALLE")
    descripcion_movimiento: str = Field(..., validation_alias="DESCRIPCION_MOVIMIENTO")
    grupo: str = Field(..., validation_alias="GRUPO")
    debito: Optional[float] = Field(None, validation_alias="DEBITO")
    credito: Optional[float] = Field(None, validation_alias="CREDITO")
    saldo_acumulado: float = Field(..., validation_alias="SALDO_ACUMULADO")
    nota: Optional[str] = Field(None, validation_alias="NOTA")


class SaldoPeriodoResponse(BaseModel):
    """Respuesta de saldo por periodo (VW_SALDO_PERIODO)."""
    model_config = ConfigDict(populate_by_name=True)

    id_estudiante: int = Field(..., validation_alias="ID_ESTUDIANTE")
    estudiante: str = Field(..., validation_alias="ESTUDIANTE")
    id_periodo: int = Field(..., validation_alias="ID_PERIODO")
    nombre_periodo: str = Field(..., validation_alias="NOMBRE_PERIODO")
    total_cobros: float = Field(..., validation_alias="TOTAL_COBROS")
    total_pagos: float = Field(..., validation_alias="TOTAL_PAGOS")
    saldo_neto: float = Field(..., validation_alias="SALDO_NETO")


class CuentaCorrienteListResponse(BaseModel):
    """Respuesta para listar detalle de cuenta corriente."""
    success: bool = Field(...)
    message: str = Field(...)
    data: List[CuentaCorrienteDetalleResponse] = Field(default=[])


class SaldoPeriodoListResponse(BaseModel):
    """Respuesta para listar saldos por periodo."""
    success: bool = Field(...)
    message: str = Field(...)
    data: List[SaldoPeriodoResponse] = Field(default=[])
