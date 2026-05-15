"""
routes/administrador.py — Endpoints para ADMINISTRADOR (Etapa 5)
Gestión de usuarios, personas, perfiles y menús.
"""

from fastapi import APIRouter, Depends, HTTPException
from app.services.permissions import require_perfil, require_any_auth
from app.schemas.persona import PersonaCreate, PersonaResponse, PersonaListResponse, PersonaDetailResponse
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse, UsuarioListResponse, UsuarioDetailResponse
from app.schemas.perfil import PerfilCreate, PerfilResponse, PerfilConPermisosResponse, PerfilListResponse, PerfilDetailResponse
from app.schemas.menu import MenuCreate, MenuResponse, MenuListResponse, MenuDetailResponse, PermisoCreate, PermisoResponse, PermisoListResponse
from app.services.persona import get_all_personas, get_persona_by_cedula, create_persona, update_persona, delete_persona
from app.services.usuario import get_all_usuarios, get_usuario_by_id, create_usuario, update_usuario, delete_usuario, reset_and_email_contrasena
from app.services.perfil import get_all_perfiles, get_perfil_by_id, get_permisos_by_perfil, create_perfil, assign_permission, remove_permission, get_all_permisos, create_permiso, delete_permiso
from app.services.menu import get_all_menus, get_menu_by_id, create_menu, update_menu, delete_menu
from app.services.database import is_fk_violation
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["administrador"])

# Solo ADMINISTRADOR puede acceder a estos endpoints
PERMISOS = ["ADMINISTRADOR"]


# ==========================================
# PERSONA
# ==========================================

@router.get("/personas", response_model=PersonaListResponse)
async def listar_personas(current_user: dict = Depends(require_any_auth)):
    """Listar todas las personas."""
    try:
        personas = get_all_personas()
        validated = [PersonaResponse.model_validate(p) for p in personas]
        return PersonaListResponse(success=True, message="Personas obtenidas", data=validated)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener personas")


@router.get("/personas/{cedula}", response_model=PersonaDetailResponse)
async def obtener_persona(cedula: int, current_user: dict = Depends(require_any_auth)):
    """Obtener persona por cédula."""
    try:
        persona = get_persona_by_cedula(cedula)
        if not persona:
            logger.error(f"✗ Persona no encontrada: {cedula}")
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        return PersonaDetailResponse(success=True, message="Persona obtenida", data=PersonaResponse.model_validate(persona))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener persona")


@router.post("/personas", response_model=PersonaDetailResponse, status_code=201)
async def crear_persona_endpoint(data: PersonaCreate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Crear nueva persona."""
    try:
        nueva = create_persona(data.cedula, data.nombre, data.apellido, data.correo, data.telefono)
        logger.info(f"✓ Usuario {current_user.get('username')} creó persona: {data.cedula}")
        return PersonaDetailResponse(success=True, message="Persona creada", data=PersonaResponse.model_validate(nueva))
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al crear persona")


@router.delete("/personas/{cedula}")
async def eliminar_persona_endpoint(cedula: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Eliminar persona. Por FK ON DELETE CASCADE, también elimina el usuario asociado."""
    try:
        if not get_persona_by_cedula(cedula):
            raise HTTPException(status_code=404, detail="Persona no encontrada")
        delete_persona(cedula)
        logger.info(f"✓ {current_user.get('username')} eliminó persona {cedula} (y su usuario)")
        return {"success": True, "message": f"Persona {cedula} eliminada (y su usuario asociado)"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error al eliminar persona: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar persona")


# ==========================================
# USUARIO
# ==========================================

@router.get("/usuarios", response_model=UsuarioListResponse)
async def listar_usuarios(current_user: dict = Depends(require_any_auth)):
    """Listar todos los usuarios."""
    try:
        usuarios = get_all_usuarios()
        validated = [UsuarioResponse.model_validate(u) for u in usuarios]
        return UsuarioListResponse(success=True, message="Usuarios obtenidos", data=validated)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener usuarios")


@router.get("/usuarios/{id_user}", response_model=UsuarioDetailResponse)
async def obtener_usuario(id_user: int, current_user: dict = Depends(require_any_auth)):
    """Obtener usuario por ID."""
    try:
        usuario = get_usuario_by_id(id_user)
        if not usuario:
            logger.error(f"✗ Usuario no encontrado: {id_user}")
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return UsuarioDetailResponse(success=True, message="Usuario obtenido", data=UsuarioResponse.model_validate(usuario))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener usuario")


@router.post("/usuarios", response_model=UsuarioDetailResponse, status_code=201)
async def crear_usuario_endpoint(data: UsuarioCreate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Crear nuevo usuario."""
    try:
        nuevo = create_usuario(
            data.username, data.contrasena, data.id_perfil, data.cedula,
            data.nombre, data.apellido, data.correo, data.telefono
        )
        logger.info(f"✓ Usuario {current_user.get('username')} creó usuario: {data.username}")
        return UsuarioDetailResponse(success=True, message="Usuario creado", data=UsuarioResponse.model_validate(nuevo))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        error_str = str(e)
        logger.error(f"✗ Error al crear usuario: {error_str}")
        if "ORA-00001" in error_str:
            if "UQ_USR_USERNAME" in error_str or "USERNAME" in error_str.upper():
                raise HTTPException(status_code=409, detail="El nombre de usuario ya está en uso.")
            if "UQ_USR_CEDULA" in error_str or "UQ_PER" in error_str:
                raise HTTPException(status_code=409, detail="Ya existe un usuario registrado con esa cédula.")
            if "CORREO" in error_str.upper():
                raise HTTPException(status_code=409, detail="El correo electrónico ya está registrado en otra persona.")
            raise HTTPException(status_code=409, detail="El registro viola una restricción de unicidad.")
        raise HTTPException(status_code=500, detail=f"Error al crear usuario: {error_str}")


@router.put("/usuarios/{id_user}", response_model=UsuarioDetailResponse)
async def actualizar_usuario_endpoint(id_user: int, data: UsuarioUpdate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Actualizar usuario."""
    try:
        usuario = get_usuario_by_id(id_user)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        update_usuario(
            id_user, data.username, data.id_perfil,
            data.nombre, data.apellido, data.correo, data.telefono
        )
        actualizado = get_usuario_by_id(id_user)
        logger.info(f"✓ Usuario {current_user.get('username')} actualizó usuario: {id_user}")
        return UsuarioDetailResponse(success=True, message="Usuario actualizado", data=UsuarioResponse.model_validate(actualizado))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al actualizar usuario")


@router.delete("/usuarios/{id_user}")
async def eliminar_usuario_endpoint(id_user: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Eliminar usuario."""
    try:
        if not get_usuario_by_id(id_user):
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        delete_usuario(id_user)
        logger.info(f"✓ Usuario {current_user.get('username')} eliminó usuario: {id_user}")
        return {"success": True, "message": f"Usuario {id_user} eliminado"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        if is_fk_violation(e):
            raise HTTPException(status_code=409, detail="No se puede eliminar el usuario: tiene datos dependientes que impiden su eliminación.")
        raise HTTPException(status_code=500, detail="Error al eliminar usuario")


@router.post("/usuarios/{id_user}/enviar-credenciales")
async def enviar_credenciales_endpoint(id_user: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Genera una nueva contraseña temporal y la envía al correo del usuario."""
    try:
        correo = reset_and_email_contrasena(id_user)
        logger.info(f"✓ {current_user.get('username')} envió credenciales al usuario {id_user}")
        return {"success": True, "message": f"Credenciales enviadas a {correo}"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"✗ Error al enviar credenciales: {e}")
        raise HTTPException(status_code=500, detail="Error al enviar las credenciales")


# ==========================================
# PERFIL
# ==========================================

@router.get("/perfiles", response_model=PerfilListResponse)
async def listar_perfiles(current_user: dict = Depends(require_any_auth)):
    """Listar todos los perfiles con sus permisos."""
    try:
        perfiles = get_all_perfiles()
        result = []
        for p in perfiles:
            permisos = get_permisos_by_perfil(p['ID_PERFIL'])
            perfil_con_permisos = PerfilConPermisosResponse(
                id_perfil=p['ID_PERFIL'],
                nombre_perfil=p['NOMBRE_PERFIL'],
                permisos=permisos
            )
            result.append(perfil_con_permisos)
        return PerfilListResponse(success=True, message="Perfiles obtenidos", data=result)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener perfiles")


@router.get("/perfiles/{id_perfil}", response_model=PerfilDetailResponse)
async def obtener_perfil(id_perfil: int, current_user: dict = Depends(require_any_auth)):
    """Obtener perfil por ID."""
    try:
        perfil = get_perfil_by_id(id_perfil)
        if not perfil:
            logger.error(f"✗ Perfil no encontrado: {id_perfil}")
            raise HTTPException(status_code=404, detail="Perfil no encontrado")
        return PerfilDetailResponse(success=True, message="Perfil obtenido", data=PerfilResponse.model_validate(perfil))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener perfil")


# ==========================================
# PERFIL — GESTIÓN DE PERMISOS
# ==========================================

@router.post("/perfiles/{id_perfil}/permisos/{id_permiso}")
async def asignar_permiso_a_perfil(id_perfil: int, id_permiso: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Asignar un permiso a un perfil (controla qué menús ve ese rol)."""
    try:
        assign_permission(id_perfil, id_permiso)
        logger.info(f"✓ {current_user.get('username')} asignó permiso {id_permiso} a perfil {id_perfil}")
        return {"success": True, "message": f"Permiso {id_permiso} asignado al perfil {id_perfil}"}
    except Exception as e:
        error_str = str(e)
        logger.error(f"✗ Error al asignar permiso: {error_str}")
        if "ORA-00001" in error_str:
            return {"success": True, "message": "El permiso ya estaba asignado"}
        raise HTTPException(status_code=500, detail="Error al asignar permiso")


@router.delete("/perfiles/{id_perfil}/permisos/{id_permiso}")
async def remover_permiso_de_perfil(id_perfil: int, id_permiso: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Remover un permiso de un perfil."""
    try:
        remove_permission(id_perfil, id_permiso)
        logger.info(f"✓ {current_user.get('username')} removió permiso {id_permiso} de perfil {id_perfil}")
        return {"success": True, "message": f"Permiso {id_permiso} removido del perfil {id_perfil}"}
    except Exception as e:
        logger.error(f"✗ Error al remover permiso: {e}")
        raise HTTPException(status_code=500, detail="Error al remover permiso")


@router.post("/perfiles", response_model=PerfilDetailResponse, status_code=201)
async def crear_perfil_endpoint(data: PerfilCreate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Crear nuevo perfil."""
    try:
        nuevo = create_perfil(data.nombre_perfil)
        logger.info(f"✓ Usuario {current_user.get('username')} creó perfil: {data.nombre_perfil}")
        return PerfilDetailResponse(success=True, message="Perfil creado", data=PerfilResponse.model_validate(nuevo))
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al crear perfil")


# ==========================================
# MENU
# ==========================================

@router.get("/menus", response_model=MenuListResponse)
async def listar_menus(current_user: dict = Depends(require_any_auth)):
    """Listar todos los menús."""
    try:
        menus = get_all_menus()
        validated = [MenuResponse.model_validate(m) for m in menus]
        return MenuListResponse(success=True, message="Menús obtenidos", data=validated)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener menús")


@router.get("/menus/{id_menu}", response_model=MenuDetailResponse)
async def obtener_menu(id_menu: int, current_user: dict = Depends(require_any_auth)):
    """Obtener menú por ID."""
    try:
        menu = get_menu_by_id(id_menu)
        if not menu:
            logger.error(f"✗ Menú no encontrado: {id_menu}")
            raise HTTPException(status_code=404, detail="Menú no encontrado")
        return MenuDetailResponse(success=True, message="Menú obtenido", data=MenuResponse.model_validate(menu))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener menú")


# DESACTIVADO EN TAREA 3: Gestión de menús es solo lectura (configuración fija del sistema)
# @router.post("/menus", response_model=MenuDetailResponse, status_code=201)
# async def crear_menu_endpoint(data: MenuCreate, current_user: dict = Depends(require_perfil(PERMISOS))):
#     """Crear nuevo menú."""
#     try:
#         nuevo = create_menu(data.nombre_funcion, data.url_acceso)
#         logger.info(f"✓ Usuario {current_user.get('username')} creó menú: {data.nombre_funcion}")
#         return MenuDetailResponse(success=True, message="Menú creado", data=MenuResponse.model_validate(nuevo))
#     except Exception as e:
#         logger.error(f"✗ Error: {e}")
#         raise HTTPException(status_code=500, detail="Error al crear menú")


# ==========================================
# PERMISO (catálogo)
# ==========================================

@router.get("/permisos", response_model=PermisoListResponse)
async def listar_permisos(current_user: dict = Depends(require_any_auth)):
    """Listar todos los permisos del catálogo."""
    try:
        permisos = get_all_permisos()
        validated = [PermisoResponse.model_validate(p) for p in permisos]
        return PermisoListResponse(success=True, message="Permisos obtenidos", data=validated)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener permisos")


@router.post("/permisos", response_model=PermisoResponse, status_code=201)
async def crear_permiso_endpoint(data: PermisoCreate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Crear un nuevo permiso en el catálogo."""
    try:
        nuevo = create_permiso(data.nombre_operacion, data.descripcion, data.id_menu)
        return PermisoResponse.model_validate(nuevo)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al crear permiso")


@router.delete("/permisos/{id_permiso}", status_code=204)
async def eliminar_permiso_endpoint(id_permiso: int, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Eliminar un permiso del catálogo."""
    try:
        delete_permiso(id_permiso)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al eliminar permiso")

