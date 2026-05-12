"""
routes/cuenta_corriente.py — Endpoints para Cuenta Corriente (Etapa 7)

Endpoints:
- GET /api/cuenta-corriente/{id_estudiante} → detalle completo
- GET /api/cuenta-corriente/{id_estudiante}/saldo → saldo por periodo
"""

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.cuenta_corriente import (
    CuentaCorrienteDetalleResponse, CuentaCorrienteListResponse,
    SaldoPeriodoResponse, SaldoPeriodoListResponse
)
from app.services import cuenta_corriente as cc_service
from app.services import movimiento as movimiento_service
from app.services.permissions import require_perfil
from typing import Dict, Any
import logging
import traceback

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/cuenta-corriente", tags=["CUENTA CORRIENTE"])

# ASISTENTE y ADMINISTRADOR pueden ver la cuenta corriente
PERMISOS = ["ASISTENTE", "ADMINISTRADOR"]


@router.get("/{id_estudiante}", response_model=CuentaCorrienteListResponse)
async def obtener_cuenta_corriente(
    id_estudiante: int,
    perfil_info: Dict[str, Any] = Depends(require_perfil(PERMISOS))
):
    """Devuelve el detalle completo de la cuenta corriente de un estudiante
    usando la vista VW_CUENTA_CORRIENTE_DETALLE."""
    try:
        movimientos = cc_service.get_cuenta_corriente_detalle(id_estudiante)

        return {
            "success": True,
            "message": f"Cuenta corriente del estudiante {id_estudiante}: {len(movimientos)} movimientos",
            "data": [CuentaCorrienteDetalleResponse.model_validate(m) for m in movimientos]
        }
    except Exception as e:
        logger.error(f"✗ Error al obtener cuenta corriente: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id_estudiante}/saldo", response_model=SaldoPeriodoListResponse)
async def obtener_saldo_periodo(
    id_estudiante: int,
    perfil_info: Dict[str, Any] = Depends(require_perfil(PERMISOS))
):
    """Devuelve el saldo por periodo de un estudiante
    usando la vista VW_SALDO_PERIODO.
    Muestra: TOTAL_COBROS - TOTAL_PAGOS = SALDO_NETO (debe ser 0 si está balanceado)."""
    try:
        saldos = cc_service.get_saldo_periodo(id_estudiante)

        return {
            "success": True,
            "message": f"Saldo del estudiante {id_estudiante}: {len(saldos)} periodos",
            "data": [SaldoPeriodoResponse.model_validate(s) for s in saldos]
        }
    except Exception as e:
        logger.error(f"✗ Error al obtener saldo: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/movimientos/{id_mov}")
async def eliminar_movimiento(
    id_mov: int,
    perfil_info: Dict[str, Any] = Depends(require_perfil(PERMISOS))
):
    """Elimina un movimiento de la cuenta corriente."""
    try:
        eliminado = movimiento_service.eliminar_movimiento(id_mov)
        if not eliminado:
            raise HTTPException(status_code=404, detail=f"Movimiento {id_mov} no encontrado")
        return {"success": True, "message": f"Movimiento {id_mov} eliminado"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error al eliminar movimiento: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
