"""
routes/administrador.py — Endpoints para ADMINISTRADOR (Etapa 5)
Gestión de usuarios, personas, perfiles y menús.
"""

from fastapi import APIRouter, Depends, HTTPException
from app.services.permissions import require_perfil
from app.schemas.persona import PersonaCreate, PersonaResponse, PersonaListResponse, PersonaDetailResponse
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioListResponse, UsuarioDetailResponse
from app.schemas.perfil import PerfilCreate, PerfilResponse, PerfilConPermisosResponse, PerfilListResponse, PerfilDetailResponse
from app.schemas.menu import MenuCreate, MenuResponse, MenuListResponse, MenuDetailResponse
from app.services.persona import get_all_personas, get_persona_by_cedula, create_persona, update_persona
from app.services.usuario import get_all_usuarios, get_usuario_by_id, create_usuario, update_usuario, delete_usuario
from app.services.perfil import get_all_perfiles, get_perfil_by_id, get_permisos_by_perfil, create_perfil, assign_permission, remove_permission
from app.services.menu import get_all_menus, get_menu_by_id, create_menu, update_menu, delete_menu
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["administrador"])

# Solo ADMINISTRADOR puede acceder a estos endpoints
PERMISOS = ["ADMINISTRADOR"]


# ==========================================
# PERSONA
# ==========================================

@router.get("/personas", response_model=PersonaListResponse)
async def listar_personas(current_user: dict = Depends(require_perfil(PERMISOS))):
    """Listar todas las personas."""
    try:
        personas = get_all_personas()
        validated = [PersonaResponse.model_validate(p) for p in personas]
        return PersonaListResponse(success=True, message="Personas obtenidas", data=validated)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener personas")


@router.get("/personas/{cedula}", response_model=PersonaDetailResponse)
async def obtener_persona(cedula: int, current_user: dict = Depends(require_perfil(PERMISOS))):
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


# ==========================================
# USUARIO
# ==========================================

@router.get("/usuarios", response_model=UsuarioListResponse)
async def listar_usuarios(current_user: dict = Depends(require_perfil(PERMISOS))):
    """Listar todos los usuarios."""
    try:
        usuarios = get_all_usuarios()
        validated = [UsuarioResponse.model_validate(u) for u in usuarios]
        return UsuarioListResponse(success=True, message="Usuarios obtenidos", data=validated)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener usuarios")


@router.get("/usuarios/{id_user}", response_model=UsuarioDetailResponse)
async def obtener_usuario(id_user: int, current_user: dict = Depends(require_perfil(PERMISOS))):
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
        nuevo = create_usuario(data.username, data.contrasena, data.id_perfil, data.cedula)
        logger.info(f"✓ Usuario {current_user.get('username')} creó usuario: {data.username}")
        return UsuarioDetailResponse(success=True, message="Usuario creado", data=UsuarioResponse.model_validate(nuevo))
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al crear usuario")


# ==========================================
# PERFIL
# ==========================================

@router.get("/perfiles", response_model=PerfilListResponse)
async def listar_perfiles(current_user: dict = Depends(require_perfil(PERMISOS))):
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
async def obtener_perfil(id_perfil: int, current_user: dict = Depends(require_perfil(PERMISOS))):
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
async def listar_menus(current_user: dict = Depends(require_perfil(PERMISOS))):
    """Listar todos los menús."""
    try:
        menus = get_all_menus()
        validated = [MenuResponse.model_validate(m) for m in menus]
        return MenuListResponse(success=True, message="Menús obtenidos", data=validated)
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al obtener menús")


@router.get("/menus/{id_menu}", response_model=MenuDetailResponse)
async def obtener_menu(id_menu: int, current_user: dict = Depends(require_perfil(PERMISOS))):
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


@router.post("/menus", response_model=MenuDetailResponse, status_code=201)
async def crear_menu_endpoint(data: MenuCreate, current_user: dict = Depends(require_perfil(PERMISOS))):
    """Crear nuevo menú."""
    try:
        nuevo = create_menu(data.nombre_funcion, data.url_acceso)
        logger.info(f"✓ Usuario {current_user.get('username')} creó menú: {data.nombre_funcion}")
        return MenuDetailResponse(success=True, message="Menú creado", data=MenuResponse.model_validate(nuevo))
    except Exception as e:
        logger.error(f"✗ Error: {e}")
        raise HTTPException(status_code=500, detail="Error al crear menú")
