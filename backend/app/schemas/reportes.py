"""
schemas/reportes.py — Esquemas Pydantic para vistas de reportes (Etapa 8)
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime


# ===== VW_LISTADO_ESTUDIANTES =====
class ListadoEstudiantesResponse(BaseModel):
    """Listado de estudiantes con programa, modalidad y monto."""
    model_config = ConfigDict(populate_by_name=True)

    id_estudiante: int = Field(..., validation_alias="ID_ESTUDIANTE")
    carnet: Optional[str] = Field(None, validation_alias="CARNET")
    nombre_estudiante: str = Field(..., validation_alias="NOMBRE_ESTUDIANTE")
    apellido_estudiante: str = Field(..., validation_alias="APELLIDO_ESTUDIANTE")
    nombre_programa: str = Field(..., validation_alias="NOMBRE_PROGRAMA")
    nombre_periodo: Optional[str] = Field(None, validation_alias="NOMBRE_PERIODO")
    modalidad: Optional[str] = Field(None, validation_alias="MODALIDAD")
    monto_total: Optional[float] = Field(None, validation_alias="MONTO_TOTAL")
    estado: Optional[str] = Field(None, validation_alias="ESTADO")


# ===== VW_INGRESO_ESPERADO =====
class IngresoEsperadoResponse(BaseModel):
    """Ingreso esperado por periodo y programa."""
    model_config = ConfigDict(populate_by_name=True)

    nombre_periodo: str = Field(..., validation_alias="NOMBRE_PERIODO")
    nombre_programa: str = Field(..., validation_alias="NOMBRE_PROGRAMA")
    total_esperado: float = Field(..., validation_alias="TOTAL_ESPERADO")


# ===== VW_PENDIENTES_PAGO =====
class PendientesPagoResponse(BaseModel):
    """Estudiantes pendientes de pago."""
    model_config = ConfigDict(populate_by_name=True)

    id_estudiante: int = Field(..., validation_alias="ID_ESTUDIANTE")
    carnet: Optional[str] = Field(None, validation_alias="CARNET")
    nombre_estudiante: str = Field(..., validation_alias="NOMBRE_ESTUDIANTE")
    apellido_estudiante: str = Field(..., validation_alias="APELLIDO_ESTUDIANTE")
    correo: Optional[str] = Field(None, validation_alias="CORREO")
    telefono: Optional[str] = Field(None, validation_alias="TELEFONO")
    id_programa: int = Field(..., validation_alias="ID_PROGRAMA")
    nombre_programa: str = Field(..., validation_alias="NOMBRE_PROGRAMA")
    nombre_periodo: str = Field(..., validation_alias="NOMBRE_PERIODO")
    total_cobrado: float = Field(..., validation_alias="TOTAL_COBRADO")
    total_pagado: float = Field(..., validation_alias="TOTAL_PAGADO")
    saldo_pendiente: float = Field(..., validation_alias="SALDO_PENDIENTE")
    estado: str = Field(..., validation_alias="ESTADO")


# ===== VW_INGRESO_REAL =====
class IngresoRealResponse(BaseModel):
    """Ingreso real recibido por periodo."""
    model_config = ConfigDict(populate_by_name=True)

    nombre_periodo: str = Field(..., validation_alias="NOMBRE_PERIODO")
    total_recaudado: float = Field(..., validation_alias="TOTAL_RECAUDADO")


# ===== VW_CARTERA =====
class CarteraResponse(BaseModel):
    """Estudiantes con crédito financiero (cartera)."""
    model_config = ConfigDict(populate_by_name=True)

    id_estudiante: int = Field(..., validation_alias="ID_ESTUDIANTE")
    carnet: Optional[str] = Field(None, validation_alias="CARNET")
    nombre_estudiante: str = Field(..., validation_alias="NOMBRE_ESTUDIANTE")
    apellido_estudiante: str = Field(..., validation_alias="APELLIDO_ESTUDIANTE")
    correo: Optional[str] = Field(None, validation_alias="CORREO")
    nombre_programa: str = Field(..., validation_alias="NOMBRE_PROGRAMA")
    nombre_periodo: str = Field(..., validation_alias="NOMBRE_PERIODO")
    valor_credito: float = Field(..., validation_alias="VALOR_CREDITO")


# ===== VW_CONSULTA_PAGOS =====
class ConsultaPagosResponse(BaseModel):
    """Consulta de pagos consolidada."""
    model_config = ConfigDict(populate_by_name=True)

    id_transaccion: int = Field(..., validation_alias="ID_TRANSACCION")
    referencia: Optional[str] = Field(None, validation_alias="REFERENCIA")
    medio_pago: Optional[str] = Field(None, validation_alias="MEDIO_PAGO")
    fecha_pago: datetime = Field(..., validation_alias="FECHA_PAGO")
    valor_pagado: float = Field(..., validation_alias="VALOR_PAGADO")
    id_mov: int = Field(..., validation_alias="ID_MOV")
    carnet: Optional[str] = Field(None, validation_alias="CARNET")
    nombre_estudiante: str = Field(..., validation_alias="NOMBRE_ESTUDIANTE")
    concepto: str = Field(..., validation_alias="CONCEPTO")
    id_periodo: int = Field(..., validation_alias="ID_PERIODO")


# ===== RESPUESTAS GENERICAS DE LISTA =====
class ReporteListResponse(BaseModel):
    """Respuesta genérica para reportes (lista de cualquier tipo)."""
    success: bool = Field(...)
    message: str = Field(...)
    data: list = Field(default=[])
