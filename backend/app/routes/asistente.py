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
from typing import Dict, Any, Optional
import logging
import traceback

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/asistente", tags=["ASISTENTE"])


# ===== VOLANTES ENDPOINTS =====

@router.get("/volantes", response_model=VolanteListResponse)
async def listar_volantes(
    id_estudiante: Optional[int] = None,
    id_periodo: Optional[int] = None,
    perfil_info: Dict[str, Any] = Depends(require_perfil(["ASISTENTE", "ADMINISTRADOR"]))
):
    """Lista volantes de matrícula. Acepta filtros opcionales por id_estudiante e id_periodo."""
    try:
        volantes = volante_service.get_all_volantes(id_estudiante=id_estudiante, id_periodo=id_periodo)
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

        # Resolver id_programa: puede venir en el body o se obtiene del estudiante
        id_programa = volante.id_programa
        if not id_programa:
            from app.services.estudiante import get_estudiante_by_id
            est = get_estudiante_by_id(volante.id_estudiante)
            if not est:
                raise ValueError(f"Estudiante {volante.id_estudiante} no encontrado")
            id_programa = est['ID_PROGRAMA']
        
        nuevo_volante = volante_service.create_volante_individual(
            id_estudiante=volante.id_estudiante,
            id_periodo=volante.id_periodo,
            id_programa=id_programa,
            modalidad=volante.modalidad,
            semestre_que_cobra=volante.semestre_que_cobra,
            asignaturas=volante.asignaturas or []
        )
        
        return {
            "success": True,
            "message": f"Volante {nuevo_volante['ID_VOLANTE']} creado exitosamente",
            "data": VolanteResponse.model_validate(nuevo_volante)
        }
    except ValueError as e:
        err_str = str(e)
        logger.warning(f"⚠ Validación fallida: {err_str}")
        if err_str.startswith("CONFLICT:"):
            raise HTTPException(status_code=409, detail=err_str[len("CONFLICT:"):].strip())
        raise HTTPException(status_code=400, detail=err_str)
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
        
        if not volante.id_programa:
            raise ValueError("id_programa es requerido para cobro masivo")
        
        resultado = volante_service.create_volante_masiva(
            id_periodo=volante.id_periodo,
            id_programa=volante.id_programa,
            modalidad=volante.modalidad,
            semestre_que_cobra=volante.semestre_que_cobra
        )
        
        ids_creados = resultado["creados"]
        errores = resultado["errores"]
        omitidos = resultado.get("omitidos", 0)
        return {
            "success": True,
            "message": f"Se crearon {len(ids_creados)} volantes. {omitidos} omitidos.",
            "data": {
                "volantes_creados": ids_creados,
                "cantidad": len(ids_creados),
                "omitidos": omitidos,
                "errores": errores
            }
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
        # Validar que el código sea un cobro válido (consulta dinámica a la BD)
        from app.services.codigo_detalle import get_all_codigos
        codigos_validos = [c["CODIGO_DETALLE"] for c in get_all_codigos() if c.get("GRUPO") == "COBRO"]
        if cobro.codigo_detalle not in codigos_validos:
            raise ValueError(f"código_detalle debe ser uno de: {', '.join(sorted(codigos_validos))}")
        
        if cobro.id_volante is None and (cobro.id_estudiante is None or cobro.id_periodo is None):
            raise ValueError("Debe proporcionar id_volante o (id_estudiante + id_periodo)")

        # Crear el movimiento de cobro
        movimiento = movimiento_service.crear_cobro_adicional(
            id_volante=cobro.id_volante,
            codigo_detalle=cobro.codigo_detalle,
            valor=cobro.valor,
            id_estudiante=cobro.id_estudiante,
            id_periodo=cobro.id_periodo
        )
        
        # Retornar el volante si existe, o None si el cobro fue cargado directo a la CC
        id_vol_resuelto = cobro.id_volante or (movimiento.get('ID_VOLANTE') if movimiento else None)
        volante = volante_service.get_volante_by_id(id_vol_resuelto) if id_vol_resuelto else None

        return {
            "success": True,
            "message": f"Cobro adicional {cobro.codigo_detalle} (${cobro.valor}) cargado a la cuenta corriente",
            "data": VolanteResponse.model_validate(volante) if volante else None
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
    """Registra un pago para un volante o para cobros adicionales sin volante."""
    try:
        if pago.id_volante is not None:
            # Ruta normal: pago asociado a un volante de matrícula
            volante = volante_service.get_volante_by_id(pago.id_volante)
            if not volante:
                raise HTTPException(status_code=404, detail=f"Volante {pago.id_volante} no encontrado")
            transaccion = movimiento_service.registrar_pago(
                id_volante=pago.id_volante,
                medio_pago=pago.medio_pago,
                valor=pago.valor,
                referencia=pago.referencia,
                codigo_detalle=pago.codigo_detalle
            )
        elif pago.id_estudiante and pago.id_periodo:
            # Ruta sin volante: estudiante con cobros adicionales pero sin matrícula
            transaccion = movimiento_service.registrar_pago(
                id_volante=None,
                medio_pago=pago.medio_pago,
                valor=pago.valor,
                referencia=pago.referencia,
                codigo_detalle=pago.codigo_detalle,
                id_estudiante_override=pago.id_estudiante,
                id_periodo_override=pago.id_periodo
            )
        else:
            raise HTTPException(status_code=400, detail="Se requiere id_volante o (id_estudiante + id_periodo)")
        
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
