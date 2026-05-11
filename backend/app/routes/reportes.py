"""
routes/reportes.py — Endpoints de reportes usando vistas de Oracle (Etapa 8)

Endpoints:
- GET /api/reportes/listado-estudiantes     → VW_LISTADO_ESTUDIANTES
- GET /api/reportes/ingreso-esperado        → VW_INGRESO_ESPERADO
- GET /api/reportes/pendientes-pago         → VW_PENDIENTES_PAGO (filtrable por programa)
- GET /api/reportes/ingreso-real            → VW_INGRESO_REAL
- GET /api/reportes/cartera                 → VW_CARTERA
- GET /api/reportes/consulta-pagos          → VW_CONSULTA_PAGOS
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.reportes import (
    ListadoEstudiantesResponse, IngresoEsperadoResponse,
    PendientesPagoResponse, IngresoRealResponse,
    CarteraResponse, ConsultaPagosResponse, ReporteListResponse
)
from app.services import reportes as reportes_service
from app.services.permissions import require_perfil
from typing import Dict, Any, Optional
import logging
import traceback

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/reportes", tags=["REPORTES"])

# Todos los perfiles con permiso VER_REPORTES pueden acceder
PERMISOS = ["ADMINISTRADOR", "SUPERVISOR", "ASISTENTE"]


@router.get("/listado-estudiantes", response_model=ReporteListResponse)
async def listado_estudiantes(
    perfil_info: Dict[str, Any] = Depends(require_perfil(PERMISOS))
):
    """Listado de estudiantes con programa, modalidad de cobro y monto."""
    try:
        datos = reportes_service.get_listado_estudiantes()
        return {
            "success": True,
            "message": f"Listado de estudiantes: {len(datos)} registros",
            "data": [ListadoEstudiantesResponse.model_validate(d) for d in datos]
        }
    except Exception as e:
        logger.error(f"✗ Error en reporte: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ingreso-esperado", response_model=ReporteListResponse)
async def ingreso_esperado(
    perfil_info: Dict[str, Any] = Depends(require_perfil(PERMISOS))
):
    """Ingreso esperado totalizado por periodo académico y programa."""
    try:
        datos = reportes_service.get_ingreso_esperado()
        return {
            "success": True,
            "message": f"Ingreso esperado: {len(datos)} registros",
            "data": [IngresoEsperadoResponse.model_validate(d) for d in datos]
        }
    except Exception as e:
        logger.error(f"✗ Error en reporte: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pendientes-pago", response_model=ReporteListResponse)
async def pendientes_pago(
    id_programa: Optional[int] = Query(None, description="ID del programa para filtrar"),
    perfil_info: Dict[str, Any] = Depends(require_perfil(PERMISOS))
):
    """Estudiantes pendientes de pago. Se puede filtrar por programa académico."""
    try:
        datos = reportes_service.get_pendientes_pago(id_programa)
        msg = f"Pendientes de pago: {len(datos)} estudiantes"
        if id_programa:
            msg += f" (programa {id_programa})"
        return {
            "success": True,
            "message": msg,
            "data": [PendientesPagoResponse.model_validate(d) for d in datos]
        }
    except Exception as e:
        logger.error(f"✗ Error en reporte: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ingreso-real", response_model=ReporteListResponse)
async def ingreso_real(
    perfil_info: Dict[str, Any] = Depends(require_perfil(PERMISOS))
):
    """Ingreso real recibido en el periodo académico."""
    try:
        datos = reportes_service.get_ingreso_real()
        return {
            "success": True,
            "message": f"Ingreso real: {len(datos)} registros",
            "data": [IngresoRealResponse.model_validate(d) for d in datos]
        }
    except Exception as e:
        logger.error(f"✗ Error en reporte: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cartera", response_model=ReporteListResponse)
async def cartera(
    perfil_info: Dict[str, Any] = Depends(require_perfil(PERMISOS))
):
    """Estudiantes con crédito financiero. Muestra valor del crédito y totalizado."""
    try:
        datos = reportes_service.get_cartera()
        return {
            "success": True,
            "message": f"Cartera: {len(datos)} estudiantes con crédito",
            "data": [CarteraResponse.model_validate(d) for d in datos]
        }
    except Exception as e:
        logger.error(f"✗ Error en reporte: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/consulta-pagos", response_model=ReporteListResponse)
async def consulta_pagos(
    perfil_info: Dict[str, Any] = Depends(require_perfil(PERMISOS))
):
    """Consulta consolidada de pagos (transacciones, movimientos y datos del estudiante)."""
    try:
        datos = reportes_service.get_consulta_pagos()
        return {
            "success": True,
            "message": f"Consulta de pagos: {len(datos)} transacciones",
            "data": [ConsultaPagosResponse.model_validate(d) for d in datos]
        }
    except Exception as e:
        logger.error(f"✗ Error en reporte: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
