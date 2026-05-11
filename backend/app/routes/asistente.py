"""
routes/asistente.py — Endpoints para gestión de cobros (ASISTENTE)
"""

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.volante import VolanteCreate, VolanteResponse, VolanteDetailResponse, VolanteListResponse
from app.schemas.movimiento import (
    CobroAdicionalCreate, PagoCreate, MovimientoResponse, 
    PagoDetailResponse, TransaccionPagoResponse, MovimientoListResponse
)
from app.services.permissions import require_perfil
from app.services import volante as volante_service
from app.services import movimiento as movimiento_service
from typing import Dict, Any
import logging
import traceback

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/asistente", tags=["ASISTENTE"])


# ===== VOLANTES ENDPOINTS =====

@router.get("/volantes", response_model=VolanteListResponse)
async def listar_volantes(perfil_info: Dict[str, Any] = Depends(require_perfil(["ASISTENTE", "ADMINISTRADOR"]))):
    """Lista todos los volantes de matrícula."""
    try:
        volantes = volante_service.get_all_volantes()
        return {
            "success": True,
            "message": f"Se obtuvieron {len(volantes)} volantes",
            "data": [VolanteResponse.model_validate(v) for v in volantes]
        }
    except Exception as e:
        logger.error(f"✗ Error al listar volantes: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/volantes/{id_volante}", response_model=VolanteDetailResponse)
async def obtener_volante(
    id_volante: int,
    perfil_info: Dict[str, Any] = Depends(require_perfil(["ASISTENTE", "ADMINISTRADOR"]))
):
    """Obtiene un volante específico."""
    try:
        volante = volante_service.get_volante_by_id(id_volante)
        if not volante:
            raise HTTPException(status_code=404, detail=f"Volante {id_volante} no encontrado")
        
        return {
            "success": True,
            "message": "Volante obtenido",
            "data": VolanteResponse.model_validate(volante)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error al obtener volante: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/volantes/individual", response_model=VolanteDetailResponse)
async def crear_volante_individual(
    volante: VolanteCreate,
    perfil_info: Dict[str, Any] = Depends(require_perfil(["ASISTENTE", "ADMINISTRADOR"]))
):
    """Crea un volante para un estudiante específico."""
    try:
        if not volante.id_estudiante:
            raise ValueError("id_estudiante requerido para generación individual")
        
        if volante.modalidad not in ["GLOBAL", "CREDITOS"]:
            raise ValueError("modalidad debe ser GLOBAL o CREDITOS")
        
        nuevo_volante = volante_service.create_volante_individual(
            id_estudiante=volante.id_estudiante,
            id_periodo=volante.id_periodo,
            id_programa=volante.id_programa,
            modalidad=volante.modalidad,
            semestre_que_cobra=volante.semestre_que_cobra
        )
        
        return {
            "success": True,
            "message": f"Volante {nuevo_volante['ID_VOLANTE']} creado exitosamente",
            "data": VolanteResponse.model_validate(nuevo_volante)
        }
    except ValueError as e:
        logger.warning(f"⚠ Validación fallida: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"✗ Error al crear volante individual: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/volantes/masiva", response_model=Dict[str, Any])
async def crear_volantes_masiva(
    volante: VolanteCreate,
    perfil_info: Dict[str, Any] = Depends(require_perfil(["ASISTENTE", "ADMINISTRADOR"]))
):
    """Crea volantes para TODOS los estudiantes de un programa."""
    try:
        if volante.modalidad not in ["GLOBAL", "CREDITOS"]:
            raise ValueError("modalidad debe ser GLOBAL o CREDITOS")
        
        ids_creados = volante_service.create_volante_masiva(
            id_periodo=volante.id_periodo,
            id_programa=volante.id_programa,
            modalidad=volante.modalidad,
            semestre_que_cobra=volante.semestre_que_cobra
        )
        
        return {
            "success": True,
            "message": f"Se crearon {len(ids_creados)} volantes masivamente",
            "data": {"volantes_creados": ids_creados, "cantidad": len(ids_creados)}
        }
    except ValueError as e:
        logger.warning(f"⚠ Validación fallida: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"✗ Error al crear volantes masiva: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== MOVIMIENTOS ENDPOINTS =====

@router.get("/volantes/{id_volante}/movimientos", response_model=MovimientoListResponse)
async def listar_movimientos_volante(
    id_volante: int,
    perfil_info: Dict[str, Any] = Depends(require_perfil(["ASISTENTE", "ADMINISTRADOR"]))
):
    """Lista todos los movimientos de un volante."""
    try:
        movimientos = movimiento_service.get_movimientos_by_volante(id_volante)
        return {
            "success": True,
            "message": f"Se obtuvieron {len(movimientos)} movimientos",
            "data": [MovimientoResponse.model_validate(m) for m in movimientos]
        }
    except Exception as e:
        logger.error(f"✗ Error al listar movimientos: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cobros-adicionales", response_model=VolanteDetailResponse)
async def crear_cobro_adicional(
    cobro: CobroAdicionalCreate,
    perfil_info: Dict[str, Any] = Depends(require_perfil(["ASISTENTE", "ADMINISTRADOR"]))
):
    """Agrega un cobro adicional a un volante existente (ej: laboratorio, examen, etc)."""
    try:
        # Validar que el código sea un cobro válido
        codigos_validos = ["PCAR", "PLAB", "PEXA", "PMAT", "PCRE"]
        if cobro.codigo_detalle not in codigos_validos:
            raise ValueError(f"código_detalle debe ser uno de: {', '.join(codigos_validos)}")
        
        # Crear el movimiento de cobro
        movimiento = movimiento_service.crear_cobro_adicional(
            id_volante=cobro.id_volante,
            codigo_detalle=cobro.codigo_detalle,
            valor=cobro.valor
        )
        
        # Retornar el volante actualizado
        volante = volante_service.get_volante_by_id(cobro.id_volante)
        
        return {
            "success": True,
            "message": f"Cobro adicional {cobro.codigo_detalle} (${cobro.valor}) agregado al volante",
            "data": VolanteResponse.model_validate(volante)
        }
    except ValueError as e:
        logger.warning(f"⚠ Validación fallida: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"✗ Error al crear cobro adicional: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pagos", response_model=PagoDetailResponse)
async def registrar_pago(
    pago: PagoCreate,
    perfil_info: Dict[str, Any] = Depends(require_perfil(["ASISTENTE", "ADMINISTRADOR"]))
):
    """Registra un pago para un volante."""
    try:
        # Validar que el volante exista
        volante = volante_service.get_volante_by_id(pago.id_volante)
        if not volante:
            raise HTTPException(status_code=404, detail=f"Volante {pago.id_volante} no encontrado")
        
        # Registrar el pago
        transaccion = movimiento_service.registrar_pago(
            id_volante=pago.id_volante,
            medio_pago=pago.medio_pago,
            valor=pago.valor,
            referencia=pago.referencia
        )
        
        return {
            "success": True,
            "message": f"Pago de ${pago.valor} registrado via {pago.medio_pago}",
            "data": TransaccionPagoResponse.model_validate(transaccion)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error al registrar pago: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/movimientos/{id_mov}", response_model=Dict[str, Any])
async def eliminar_movimiento(
    id_mov: int,
    perfil_info: Dict[str, Any] = Depends(require_perfil(["ASISTENTE", "ADMINISTRADOR"]))
):
    """Elimina un movimiento. Si es el movimiento principal, se elimina el volante."""
    try:
        eliminado = movimiento_service.eliminar_movimiento(id_mov)
        
        if not eliminado:
            raise HTTPException(status_code=404, detail=f"Movimiento {id_mov} no encontrado")
        
        return {
            "success": True,
            "message": f"Movimiento {id_mov} eliminado correctamente"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error al eliminar movimiento: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))
