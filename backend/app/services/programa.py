"""
services/programa.py — Lógica de negocio para PROGRAMA_ACADEMICO

Operaciones:
- Listar todos los programas
- Crear un nuevo programa
- Obtener programa por ID
- Actualizar programa
- Eliminar programa
"""

from app.services.database import execute_query, execute_update
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_all_programas() -> List[Dict[str, Any]]:
    """
    Obtiene todos los programas académicos.
    
    Returns:
        Lista de diccionarios con los programas
        
    Raises:
        Exception: Si hay error en la BD
    """
    try:
        query = "SELECT ID_PROGRAMA, NOMBRE_PROGRAMA, CODIGO_PROGRAMA FROM PROGRAMA_ACADEMICO ORDER BY ID_PROGRAMA"
        results = execute_query(query)
        logger.info(f"✓ Se obtuvieron {len(results)} programas")
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener programas: {e}")
        raise


def get_programa_by_id(id_programa: int) -> Optional[Dict[str, Any]]:
    """
    Obtiene un programa por ID.
    
    Args:
        id_programa: ID del programa
        
    Returns:
        Diccionario con los datos del programa o None si no existe
        
    Raises:
        Exception: Si hay error en la BD
    """
    try:
        query = "SELECT ID_PROGRAMA, NOMBRE_PROGRAMA, CODIGO_PROGRAMA FROM PROGRAMA_ACADEMICO WHERE ID_PROGRAMA = :id"
        results = execute_query(query, {"id": id_programa})
        
        if results:
            logger.info(f"✓ Programa obtenido: ID {id_programa}")
            return results[0]
        else:
            logger.warning(f"✗ Programa no encontrado: ID {id_programa}")
            return None
    except Exception as e:
        logger.error(f"✗ Error al obtener programa: {e}")
        raise


def create_programa(nombre_programa: str, codigo_programa: str) -> Dict[str, Any]:
    """
    Crea un nuevo programa académico.
    """
    try:
        seq_result = execute_query("SELECT SEQ_PROGRAMA.NEXTVAL AS ID_PROGRAMA FROM DUAL")
        new_id = seq_result[0]['ID_PROGRAMA']

        query = """
            INSERT INTO PROGRAMA_ACADEMICO (ID_PROGRAMA, NOMBRE_PROGRAMA, CODIGO_PROGRAMA)
            VALUES (:id, :nombre, :codigo)
        """
        execute_update(query, {"id": new_id, "nombre": nombre_programa, "codigo": codigo_programa.upper()})

        return {
            "ID_PROGRAMA": new_id,
            "NOMBRE_PROGRAMA": nombre_programa,
            "CODIGO_PROGRAMA": codigo_programa.upper()
        }
    except Exception as e:
        logger.error(f"✗ Error al crear programa: {e}")
        raise


def update_programa(id_programa: int, nombre_programa: Optional[str] = None, codigo_programa: Optional[str] = None) -> bool:
    """
    Actualiza un programa académico.
    """
    try:
        sets = []
        params: Dict[str, Any] = {"id": id_programa}
        if nombre_programa is not None:
            sets.append("NOMBRE_PROGRAMA = :nombre")
            params["nombre"] = nombre_programa
        if codigo_programa is not None:
            sets.append("CODIGO_PROGRAMA = :codigo")
            params["codigo"] = codigo_programa.upper()
        if not sets:
            return False
        query = f"UPDATE PROGRAMA_ACADEMICO SET {', '.join(sets)} WHERE ID_PROGRAMA = :id"
        affected = execute_update(query, params)
        if affected > 0:
            logger.info(f"✓ Programa actualizado: ID {id_programa}")
            return True
        logger.warning(f"✗ Programa no encontrado para actualizar: ID {id_programa}")
        return False
    except Exception as e:
        logger.error(f"✗ Error al actualizar programa: {e}")
        raise


def delete_programa(id_programa: int) -> bool:
    """
    Elimina un programa académico.
    
    NOTA: Esto solo funciona si no hay registros dependientes.
    Oracle validará las foreign keys.
    
    Args:
        id_programa: ID del programa
        
    Returns:
        True si se eliminó correctamente
        
    Raises:
        Exception: Si hay error en la BD (ej: hay dependencias)
    """
def delete_programa(id_programa: int) -> bool:
    """
    Elimina un programa académico.
    Oracle CASCADE elimina: ESTUDIANTE → CUENTA_CORRIENTE → MOVIMIENTO → TRANSACCION_PAGO,
    VOLANTE_MATRICULA → VOLANTE_MATRICULA_ASIGNATURA, REGLA_COBRO, PLAN_ESTUDIO → PLAN_ESTUDIO_ASIGNATURA.
    """
    try:
        query = "DELETE FROM PROGRAMA_ACADEMICO WHERE ID_PROGRAMA = :id"
        affected = execute_update(query, {"id": id_programa})

        if affected > 0:
            logger.info(f"✓ Programa eliminado: ID {id_programa}")
            return True
        else:
            logger.warning(f"✗ Programa no encontrado para eliminar: ID {id_programa}")
            return False
    except Exception as e:
        logger.error(f"✗ Error al eliminar programa: {e}")
        raise
