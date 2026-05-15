"""
routes/supervisor.py — Endpoints para SUPERVISOR CRUD

Gestiona:
- Programas académicos
- Asignaturas  
- Períodos académicos
- Planes de estudio
- Plan estudio asignaturas
- Reglas de cobro
- Códigos de detalle
- Estudiantes
"""

from fastapi import APIRouter, HTTPException, status, Depends
from datetime import date

# Schemas
from app.schemas.programa import ProgramaCreate, ProgramaUpdate, ProgramaResponse, ProgramaListResponse, ProgramaDetailResponse
from app.schemas.asignatura import AsignaturaCreate, AsignaturaUpdate, AsignaturaResponse, AsignaturaListResponse, AsignaturaDetailResponse
from app.schemas.periodo import PeriodoCreate, PeriodoUpdate, PeriodoResponse, PeriodoListResponse, PeriodoDetailResponse
from app.schemas.estudiante import EstudianteCreate, EstudianteUpdate, EstudianteResponse, EstudianteListResponse, EstudianteDetailResponse
from app.schemas.plan_estudio import PlanEstudioCreate, PlanEstudioResponse, PlanEstudioListResponse
from app.schemas.plan_estudio_asignatura import PlanEstudioAsignaturaCreate, PlanEstudioAsignaturaResponse, PlanEstudioAsignaturaListResponse
from app.schemas.regla_cobro import ReglaCobroCreate, ReglaCobroUpdate, ReglaCobroResponse, ReglaCobroListResponse
from app.schemas.codigo_detalle import CodigoDetalleCreate, CodigoDetalleUpdate, CodigoDetalleResponse, CodigoDetalleListResponse, CodigoDetalleDetailResponse

# Services
from app.services.programa import get_all_programas, get_programa_by_id, create_programa, update_programa, delete_programa
from app.services.asignatura import get_all_asignaturas, get_asignatura_by_id, create_asignatura, update_asignatura, delete_asignatura
from app.services.periodo import get_all_periodos, get_periodo_by_id, create_periodo, update_periodo, delete_periodo
from app.services.estudiante import get_all_estudiantes, get_estudiante_by_id, create_estudiante, update_estudiante, delete_estudiante
from app.services.plan_estudio import get_planes_by_programa, create_plan
from app.services.plan_estudio_asignatura import get_asignaturas_by_plan, add_asignatura_to_plan, remove_asignatura_from_plan
from app.services.regla_cobro import get_reglas_by_programa_periodo, create_regla, update_regla, delete_regla
from app.services.codigo_detalle import get_all_codigos, get_codigo_by_id, create_codigo, update_codigo, delete_codigo

from app.services.permissions import require_perfil
from app.services.database import is_fk_violation
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["SUPERVISOR"])
PERMISOS = ["SUPERVISOR", "ADMINISTRADOR", "ASISTENTE"]


# ==========================================
# PROGRAMA ACADEMICO
# ==========================================

@router.get("/programas", response_model=ProgramaListResponse)
async def listar_programas(current_user: dict = Depends(require_perfil(PERMISOS))):
    """Listar todos los programas académicos."""
    try:
        programas = get_all_programas()
        validated = [ProgramaResponse.model_validate(p) for p in programas]
        return ProgramaListResponse(success=True, message="Programas obtenidos", data=validated)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener programas")


@router.get("/programas/{id_programa}", response_model=ProgramaDetailResponse)
async def obtener_programa(id_programa: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Obtener programa por ID."""
    try:
        programa = get_programa_by_id(id_programa)
        if not programa:
            raise HTTPException(status_code=404, detail=f"Programa {id_programa} no encontrado")
        return ProgramaDetailResponse(success=True, message="Programa obtenido", data=ProgramaResponse.model_validate(programa))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener programa")


@router.post("/programas", response_model=ProgramaDetailResponse, status_code=201)
async def crear_programa_endpoint(data: ProgramaCreate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Crear nuevo programa."""
    try:
        if not data.nombre_programa.strip():
            raise HTTPException(status_code=400, detail="Nombre no puede estar vacío")
        if not data.codigo_programa.strip():
            raise HTTPException(status_code=400, detail="Código no puede estar vacío")
        nuevo = create_programa(data.nombre_programa, data.codigo_programa)
        logger.info(f"✓ Usuario {current_user.get('username')} creó programa: {nuevo['ID_PROGRAMA']}")
        return ProgramaDetailResponse(success=True, message="Programa creado", data=ProgramaResponse.model_validate(nuevo), status_code=201)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al crear programa")


# ==========================================
# ASIGNATURA
# ==========================================

@router.get("/asignaturas", response_model=AsignaturaListResponse)
async def listar_asignaturas(current_user: dict = Depends(require_perfil(PERMISOS))):
    """Listar todas las asignaturas."""
    try:
        asignaturas = get_all_asignaturas()
        validated = [AsignaturaResponse.model_validate(a) for a in asignaturas]
        return AsignaturaListResponse(success=True, message="Asignaturas obtenidas", data=validated)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener asignaturas")


@router.get("/asignaturas/{id_asignatura}", response_model=AsignaturaDetailResponse)
async def obtener_asignatura(id_asignatura: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Obtener asignatura por ID."""
    try:
        asignatura = get_asignatura_by_id(id_asignatura)
        if not asignatura:
            raise HTTPException(status_code=404, detail=f"Asignatura {id_asignatura} no encontrada")
        return AsignaturaDetailResponse(success=True, message="Asignatura obtenida", data=AsignaturaResponse.model_validate(asignatura))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener asignatura")


@router.post("/asignaturas", response_model=AsignaturaDetailResponse, status_code=201)
async def crear_asignatura_endpoint(data: AsignaturaCreate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Crear nueva asignatura."""
    try:
        nueva = create_asignatura(data.nombre, data.cant_creditos)
        logger.info(f"✓ Usuario {current_user.get('username')} creó asignatura: {nueva['ID_ASIGNATURA']}")
        return AsignaturaDetailResponse(success=True, message="Asignatura creada", data=AsignaturaResponse.model_validate(nueva))
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al crear asignatura")


# ==========================================
# PERIODO ACADEMICO
# ==========================================

@router.get("/periodos", response_model=PeriodoListResponse)
async def listar_periodos(current_user: dict = Depends(require_perfil(PERMISOS))):
    """Listar todos los períodos académicos."""
    try:
        periodos = get_all_periodos()
        validated = [PeriodoResponse.model_validate(p) for p in periodos]
        return PeriodoListResponse(success=True, message="Períodos obtenidos", data=validated)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener períodos")


@router.get("/periodos/{id_periodo}", response_model=PeriodoDetailResponse)
async def obtener_periodo(id_periodo: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Obtener período por ID."""
    try:
        periodo = get_periodo_by_id(id_periodo)
        if not periodo:
            raise HTTPException(status_code=404, detail=f"Período {id_periodo} no encontrado")
        return PeriodoDetailResponse(success=True, message="Período obtenido", data=PeriodoResponse.model_validate(periodo))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener período")


@router.post("/periodos", response_model=PeriodoDetailResponse, status_code=201)
async def crear_periodo_endpoint(data: PeriodoCreate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Crear nuevo período."""
    try:
        nuevo = create_periodo(data.nombre_periodo, str(data.fecha_inicio), str(data.fecha_fin))
        logger.info(f"✓ Usuario {current_user.get('username')} creó período: {nuevo['ID_PERIODO']}")
        logger.debug(f"Datos para validar: {nuevo}")
        validated = PeriodoResponse.model_validate(nuevo)
        return PeriodoDetailResponse(success=True, message="Periodo creado", data=validated)
    except Exception as e:
        logger.error(f"✗ Error en crear_periodo_endpoint: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al crear período: {str(e)}")


# ==========================================
# ESTUDIANTE
# ==========================================

@router.get("/estudiantes", response_model=EstudianteListResponse)
async def listar_estudiantes(current_user: dict = Depends(require_perfil(PERMISOS))):
    """Listar todos los estudiantes."""
    try:
        estudiantes = get_all_estudiantes()
        validated = [EstudianteResponse.model_validate(e) for e in estudiantes]
        return EstudianteListResponse(success=True, message="Estudiantes obtenidos", data=validated)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener estudiantes")


@router.get("/estudiantes/{id_estudiante}", response_model=EstudianteDetailResponse)
async def obtener_estudiante(id_estudiante: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Obtener estudiante por ID."""
    try:
        estudiante = get_estudiante_by_id(id_estudiante)
        if not estudiante:
            raise HTTPException(status_code=404, detail=f"Estudiante {id_estudiante} no encontrado")
        return EstudianteDetailResponse(success=True, message="Estudiante obtenido", data=EstudianteResponse.model_validate(estudiante))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener estudiante")


@router.post("/estudiantes", response_model=EstudianteDetailResponse, status_code=201)
async def crear_estudiante_endpoint(data: EstudianteCreate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Crear nuevo estudiante."""
    try:
        nuevo = create_estudiante(data.nombre, data.apellido, data.telefono, data.correo, data.id_programa)
        logger.info(f"✓ Usuario {current_user.get('username')} creó estudiante: {nuevo['ID_ESTUDIANTE']}")
        return EstudianteDetailResponse(success=True, message="Estudiante creado", data=EstudianteResponse.model_validate(nuevo))
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al crear estudiante")


@router.put("/estudiantes/{id_estudiante}", response_model=EstudianteDetailResponse)
async def actualizar_estudiante_endpoint(id_estudiante: int, data: EstudianteUpdate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Actualizar estudiante existente."""
    try:
        # Verificar que el estudiante existe
        estudiante = get_estudiante_by_id(id_estudiante)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        
        # Usar valores existentes si no se proporcionan nuevos
        nombre = data.nombre if data.nombre else estudiante['NOMBRE']
        apellido = data.apellido if data.apellido else estudiante['APELLIDO']
        telefono = data.telefono if data.telefono is not None else estudiante.get('TELEFONO')
        correo = data.correo if data.correo is not None else estudiante.get('CORREO')
        
        update_estudiante(id_estudiante, nombre, apellido, telefono, correo, data.id_programa)
        logger.info(f"✓ Usuario {current_user.get('username')} actualizó estudiante: {id_estudiante}")
        
        # Obtener y devolver el estudiante actualizado
        estudiante_actualizado = get_estudiante_by_id(id_estudiante)
        return EstudianteDetailResponse(success=True, message="Estudiante actualizado", data=EstudianteResponse.model_validate(estudiante_actualizado))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar estudiante")


# ==========================================
# PLAN DE ESTUDIO
# ==========================================

@router.get("/programas/{id_programa}/planes", response_model=PlanEstudioListResponse)
async def listar_planes(id_programa: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Listar todos los semestres de un programa."""
    try:
        planes = get_planes_by_programa(id_programa)
        validated = [PlanEstudioResponse.model_validate(p) for p in planes]
        return PlanEstudioListResponse(success=True, message="Planes obtenidos", data=validated)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener planes")


@router.post("/programas/{id_programa}/planes", response_model=PlanEstudioListResponse, status_code=201)
async def agregar_semestre(id_programa: int, data: PlanEstudioCreate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Agregar semestre a un programa."""
    try:
        nuevo = create_plan(data.semestre, id_programa)
        logger.info(f"[OK] Usuario {current_user.get('username')} agrego semestre {data.semestre} al programa {id_programa}")
        return PlanEstudioListResponse(success=True, message="Semestre agregado", data=[PlanEstudioResponse.model_validate(nuevo)])
    except Exception as e:
        logger.error(f"[ERROR] agregar_semestre: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al agregar semestre: {str(e)}")


# ==========================================
# PLAN ESTUDIO ASIGNATURA
# ==========================================

@router.get("/programas/{id_programa}/planes/{semestre}/asignaturas", response_model=PlanEstudioAsignaturaListResponse)
async def listar_asignaturas_plan(id_programa: int, semestre: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Listar asignaturas de un semestre."""
    try:
        asignaturas = get_asignaturas_by_plan(semestre, id_programa)
        validated = [PlanEstudioAsignaturaResponse.model_validate(a) for a in asignaturas]
        return PlanEstudioAsignaturaListResponse(success=True, message="Asignaturas obtenidas", data=validated)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener asignaturas")


@router.post("/programas/{id_programa}/planes/{semestre}/asignaturas", response_model=PlanEstudioAsignaturaListResponse, status_code=201)
async def agregar_asignatura_plan(id_programa: int, semestre: int, data: PlanEstudioAsignaturaCreate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Agregar asignatura a un semestre."""
    try:
        nuevo = add_asignatura_to_plan(semestre, id_programa, data.id_asignatura)
        logger.info(f"[OK] Usuario {current_user.get('username')} agrego asignatura {data.id_asignatura} al semestre {semestre}")
        return PlanEstudioAsignaturaListResponse(success=True, message="Asignatura agregada", data=[PlanEstudioAsignaturaResponse.model_validate(nuevo)])
    except Exception as e:
        logger.error(f"[ERROR] agregar_asignatura_plan: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al agregar asignatura: {str(e)}")


# ==========================================
# REGLA DE COBRO
# ==========================================

@router.get("/programas/{id_programa}/periodos/{id_periodo}/reglas", response_model=ReglaCobroListResponse)
async def listar_reglas(id_programa: int, id_periodo: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Listar reglas de cobro de un programa en un período."""
    try:
        reglas = get_reglas_by_programa_periodo(id_programa, id_periodo)
        validated = [ReglaCobroResponse.model_validate(r) for r in reglas]
        return ReglaCobroListResponse(success=True, message="Reglas obtenidas", data=validated)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener reglas")


@router.post("/programas/{id_programa}/periodos/{id_periodo}/reglas", response_model=ReglaCobroListResponse, status_code=201)
async def crear_regla_endpoint(id_programa: int, id_periodo: int, data: ReglaCobroCreate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Crear nueva regla de cobro."""
    try:
        # Aplicar restricción de negocio: solo pasar el valor correspondiente a la modalidad
        if data.modalidad == "GLOBAL":
            valor_credito = None
            valor_global = data.valor_global
        else:  # CREDITOS
            valor_credito = data.valor_credito
            valor_global = None
        
        nueva = create_regla(data.modalidad, id_programa, id_periodo, valor_credito, valor_global)
        logger.info(f"✓ Usuario {current_user.get('username')} creó regla {data.modalidad}")
        return ReglaCobroListResponse(success=True, message="Regla creada", data=[ReglaCobroResponse.model_validate(nueva)])
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al crear regla")


@router.put("/programas/{id_programa}/periodos/{id_periodo}/reglas/{modalidad}", response_model=ReglaCobroListResponse)
async def actualizar_regla_endpoint(id_programa: int, id_periodo: int, modalidad: str, data: ReglaCobroUpdate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Actualizar valores de una regla de cobro."""
    try:
        mod = modalidad.upper()
        updated = update_regla(mod, id_programa, id_periodo, data.valor_credito, data.valor_global)
        if not updated:
            raise HTTPException(status_code=404, detail="Regla no encontrada")
        reglas = get_reglas_by_programa_periodo(id_programa, id_periodo)
        regla = next((r for r in reglas if r['MODALIDAD'] == mod), None)
        if not regla:
            raise HTTPException(status_code=404, detail="Regla no encontrada tras actualizar")
        logger.info(f"✓ Usuario {current_user.get('username')} actualizó regla {mod}")
        return ReglaCobroListResponse(success=True, message="Regla actualizada", data=[ReglaCobroResponse.model_validate(regla)])
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar regla: {str(e)}")


# ==========================================
# CODIGO DETALLE
# ==========================================

@router.get("/codigos", response_model=CodigoDetalleListResponse)
async def listar_codigos(current_user: dict = Depends(require_perfil(PERMISOS))):
    """Listar todos los códigos de detalle."""
    try:
        codigos = get_all_codigos()
        validated = [CodigoDetalleResponse.model_validate(c) for c in codigos]
        return CodigoDetalleListResponse(success=True, message="Códigos obtenidos", data=validated)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener códigos")


@router.get("/codigos/{codigo_detalle}", response_model=CodigoDetalleDetailResponse)
async def obtener_codigo(codigo_detalle: str, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Obtener código por ID."""
    try:
        codigo = get_codigo_by_id(codigo_detalle)
        if not codigo:
            raise HTTPException(status_code=404, detail=f"Código {codigo_detalle} no encontrado")
        return CodigoDetalleDetailResponse(success=True, message="Código obtenido", data=CodigoDetalleResponse.model_validate(codigo))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener código")


@router.post("/codigos", response_model=CodigoDetalleDetailResponse, status_code=201)
async def crear_codigo_endpoint(data: CodigoDetalleCreate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Crear nuevo código de detalle."""
    try:
        nuevo = create_codigo(data.codigo_detalle, data.grupo, data.descripcion, data.valor_defecto)
        logger.info(f"[OK] Usuario {current_user.get('username')} creó código: {nuevo['CODIGO_DETALLE']}")
        return CodigoDetalleDetailResponse(success=True, message="Codigo creado", data=CodigoDetalleResponse.model_validate(nuevo))
    except Exception as e:
        logger.error(f"[ERROR] crear_codigo_endpoint: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error al crear código: {str(e)}")


@router.put("/codigos/{codigo_detalle}", response_model=CodigoDetalleDetailResponse)
async def actualizar_codigo_endpoint(codigo_detalle: str, data: CodigoDetalleUpdate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Actualizar un código de detalle."""
    try:
        codigo = get_codigo_by_id(codigo_detalle)
        if not codigo:
            raise HTTPException(status_code=404, detail=f"Código {codigo_detalle} no encontrado")
        nueva_desc = data.descripcion if data.descripcion is not None else codigo['DESCRIPCION']
        if codigo['GRUPO'] == 'PAGO':
            if data.valor_defecto is not None and data.valor_defecto > 0:
                raise HTTPException(status_code=400, detail="Los códigos de tipo PAGO no pueden tener un valor por defecto.")
            nuevo_val = None
        else:
            # Si el campo fue enviado explícitamente (incluso como null), usar ese valor.
            # Si no fue enviado en el body, conservar el valor actual de la BD.
            if 'valor_defecto' in data.model_fields_set:
                nuevo_val = data.valor_defecto  # None = el usuario lo borró intencionalmente
            else:
                nuevo_val = codigo.get('VALOR_DEFECTO')
        update_codigo(codigo_detalle, nueva_desc, nuevo_val)
        actualizado = get_codigo_by_id(codigo_detalle)
        return CodigoDetalleDetailResponse(success=True, message="Código actualizado", data=CodigoDetalleResponse.model_validate(actualizado))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar código: {str(e)}")


@router.delete("/codigos/{codigo_detalle}")
async def eliminar_codigo_endpoint(codigo_detalle: str, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Eliminar un código de detalle."""
    try:
        if not get_codigo_by_id(codigo_detalle):
            raise HTTPException(status_code=404, detail=f"Código {codigo_detalle} no encontrado")
        delete_codigo(codigo_detalle)
        return {"success": True, "message": f"Código {codigo_detalle} eliminado"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        if is_fk_violation(e):
            raise HTTPException(
                status_code=409,
                detail=f"No se puede eliminar el código '{codigo_detalle}': tiene movimientos financieros registrados (cobros o pagos). Los códigos con historial no pueden eliminarse."
            )
        raise HTTPException(status_code=500, detail=f"Error al eliminar código: {str(e)}")


# ==========================================
# PROGRAMA — PUT y DELETE
# ==========================================

@router.put("/programas/{id_programa}", response_model=ProgramaDetailResponse)
async def actualizar_programa_endpoint(id_programa: int, data: ProgramaUpdate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Actualizar programa académico."""
    try:
        programa = get_programa_by_id(id_programa)
        if not programa:
            raise HTTPException(status_code=404, detail=f"Programa {id_programa} no encontrado")
        update_programa(id_programa, data.nombre_programa or None, data.codigo_programa or None)
        actualizado = get_programa_by_id(id_programa)
        return ProgramaDetailResponse(success=True, message="Programa actualizado", data=ProgramaResponse.model_validate(actualizado))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar programa: {str(e)}")


@router.delete("/programas/{id_programa}")
async def eliminar_programa_endpoint(id_programa: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Eliminar programa académico."""
    try:
        if not get_programa_by_id(id_programa):
            raise HTTPException(status_code=404, detail=f"Programa {id_programa} no encontrado")
        delete_programa(id_programa)
        return {"success": True, "message": f"Programa {id_programa} eliminado"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        if is_fk_violation(e):
            raise HTTPException(status_code=409, detail="No se puede eliminar el programa: tiene datos dependientes que impiden su eliminación.")
        raise HTTPException(status_code=500, detail=f"Error al eliminar programa: {str(e)}")


# ==========================================
# ASIGNATURA — PUT y DELETE
# ==========================================

@router.put("/asignaturas/{id_asignatura}", response_model=AsignaturaDetailResponse)
async def actualizar_asignatura_endpoint(id_asignatura: int, data: AsignaturaUpdate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Actualizar asignatura."""
    try:
        asignatura = get_asignatura_by_id(id_asignatura)
        if not asignatura:
            raise HTTPException(status_code=404, detail=f"Asignatura {id_asignatura} no encontrada")
        nuevo_nombre = data.nombre if data.nombre is not None else asignatura['NOMBRE']
        nuevos_creditos = data.cant_creditos if data.cant_creditos is not None else asignatura['CANT_CREDITOS']
        update_asignatura(id_asignatura, nuevo_nombre, nuevos_creditos)
        actualizada = get_asignatura_by_id(id_asignatura)
        return AsignaturaDetailResponse(success=True, message="Asignatura actualizada", data=AsignaturaResponse.model_validate(actualizada))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar asignatura: {str(e)}")


@router.delete("/asignaturas/{id_asignatura}")
async def eliminar_asignatura_endpoint(id_asignatura: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Eliminar asignatura."""
    try:
        if not get_asignatura_by_id(id_asignatura):
            raise HTTPException(status_code=404, detail=f"Asignatura {id_asignatura} no encontrada")
        delete_asignatura(id_asignatura)
        return {"success": True, "message": f"Asignatura {id_asignatura} eliminada"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        if is_fk_violation(e):
            raise HTTPException(status_code=409, detail="No se puede eliminar la asignatura: tiene datos dependientes que impiden su eliminación.")
        raise HTTPException(status_code=500, detail=f"Error al eliminar asignatura: {str(e)}")


# ==========================================
# PERIODO — PUT y DELETE
# ==========================================

@router.put("/periodos/{id_periodo}", response_model=PeriodoDetailResponse)
async def actualizar_periodo_endpoint(id_periodo: int, data: PeriodoUpdate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Actualizar período académico."""
    try:
        periodo = get_periodo_by_id(id_periodo)
        if not periodo:
            raise HTTPException(status_code=404, detail=f"Período {id_periodo} no encontrado")
        nuevo_nombre = data.nombre_periodo if data.nombre_periodo is not None else periodo['NOMBRE_PERIODO']
        nueva_inicio = str(data.fecha_inicio) if data.fecha_inicio is not None else str(periodo['FECHA_INICIO'])
        nueva_fin = str(data.fecha_fin) if data.fecha_fin is not None else str(periodo['FECHA_FIN'])
        update_periodo(id_periodo, nuevo_nombre, nueva_inicio, nueva_fin)
        actualizado = get_periodo_by_id(id_periodo)
        return PeriodoDetailResponse(success=True, message="Período actualizado", data=PeriodoResponse.model_validate(actualizado))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar período: {str(e)}")


@router.delete("/periodos/{id_periodo}")
async def eliminar_periodo_endpoint(id_periodo: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Eliminar período académico."""
    try:
        if not get_periodo_by_id(id_periodo):
            raise HTTPException(status_code=404, detail=f"Período {id_periodo} no encontrado")
        delete_periodo(id_periodo)
        return {"success": True, "message": f"Período {id_periodo} eliminado"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        if is_fk_violation(e):
            raise HTTPException(status_code=409, detail="No se puede eliminar el período: tiene datos dependientes que impiden su eliminación.")
        raise HTTPException(status_code=500, detail=f"Error al eliminar período: {str(e)}")


# ==========================================
# ESTUDIANTE — DELETE
# ==========================================

@router.delete("/estudiantes/{id_estudiante}")
async def eliminar_estudiante_endpoint(id_estudiante: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Eliminar estudiante."""
    try:
        if not get_estudiante_by_id(id_estudiante):
            raise HTTPException(status_code=404, detail=f"Estudiante {id_estudiante} no encontrado")
        delete_estudiante(id_estudiante)
        return {"success": True, "message": f"Estudiante {id_estudiante} eliminado"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        if is_fk_violation(e):
            raise HTTPException(status_code=409, detail="No se puede eliminar el estudiante: tiene datos dependientes que impiden su eliminación.")
        raise HTTPException(status_code=500, detail=f"Error al eliminar estudiante: {str(e)}")


# ==========================================
# PLAN ESTUDIO ASIGNATURA — DELETE
# ==========================================

@router.delete("/programas/{id_programa}/planes/{semestre}/asignaturas/{id_asignatura}")
async def quitar_asignatura_plan(id_programa: int, semestre: int, id_asignatura: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Quitar una asignatura de un semestre del plan de estudio."""
    try:
        eliminado = remove_asignatura_from_plan(semestre, id_programa, id_asignatura)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Asignatura no encontrada en el plan")
        return {"success": True, "message": f"Asignatura {id_asignatura} quitada del semestre {semestre}"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        if is_fk_violation(e):
            raise HTTPException(status_code=409, detail="No se puede quitar la asignatura del plan: tiene datos dependientes que impiden su eliminación.")
        raise HTTPException(status_code=500, detail=f"Error al quitar asignatura: {str(e)}")


# ==========================================
# REGLA COBRO — DELETE
# ==========================================

@router.delete("/programas/{id_programa}/periodos/{id_periodo}/reglas/{modalidad}")
async def eliminar_regla_endpoint(id_programa: int, id_periodo: int, modalidad: str, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Eliminar regla de cobro."""
    try:
        eliminado = delete_regla(modalidad.upper(), id_programa, id_periodo)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Regla no encontrada")
        return {"success": True, "message": f"Regla {modalidad} eliminada"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error al eliminar regla: {str(e)}")
