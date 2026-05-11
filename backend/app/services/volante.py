"""
services/volante.py — Lógica de negocio para VOLANTE_MATRICULA
"""

from app.services.database import execute_query, execute_update
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def get_all_volantes() -> List[Dict[str, Any]]:
    """Obtiene todos los volantes."""
    try:
        query = """
            SELECT ID_VOLANTE, SEMESTRE_QUE_COBRA, FECHA_GENERACION, 
                   TIPO_GENERACION, MONTO_TOTAL, ID_ESTUDIANTE, ID_PERIODO, MODALIDAD, ID_PROGRAMA
            FROM VOLANTE_MATRICULA ORDER BY ID_VOLANTE DESC
        """
        results = execute_query(query)
        logger.info(f"✓ Se obtuvieron {len(results)} volantes")
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener volantes: {e}")
        raise


def get_volante_by_id(id_volante: int) -> Optional[Dict[str, Any]]:
    """Obtiene un volante por ID."""
    try:
        query = """
            SELECT ID_VOLANTE, SEMESTRE_QUE_COBRA, FECHA_GENERACION, 
                   TIPO_GENERACION, MONTO_TOTAL, ID_ESTUDIANTE, ID_PERIODO, MODALIDAD, ID_PROGRAMA
            FROM VOLANTE_MATRICULA WHERE ID_VOLANTE = :id
        """
        results = execute_query(query, {"id": id_volante})
        return results[0] if results else None
    except Exception as e:
        logger.error(f"✗ Error al obtener volante: {e}")
        raise


def get_volantes_by_estudiante(id_estudiante: int) -> List[Dict[str, Any]]:
    """Obtiene todos los volantes de un estudiante."""
    try:
        query = """
            SELECT ID_VOLANTE, SEMESTRE_QUE_COBRA, FECHA_GENERACION, 
                   TIPO_GENERACION, MONTO_TOTAL, ID_ESTUDIANTE, ID_PERIODO, MODALIDAD, ID_PROGRAMA
            FROM VOLANTE_MATRICULA WHERE ID_ESTUDIANTE = :id_est
            ORDER BY FECHA_GENERACION DESC
        """
        results = execute_query(query, {"id_est": id_estudiante})
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener volantes del estudiante: {e}")
        raise


def create_volante_individual(id_estudiante: int, id_periodo: int, id_programa: int, 
                             modalidad: str, semestre_que_cobra: int) -> Dict[str, Any]:
    """Crea un volante individual. El trigger TR_CALCULAR_MONTO_VOLANTE calculará el MONTO_TOTAL."""
    try:
        # Obtener el siguiente ID
        seq_result = execute_query("SELECT SEQ_VOLANTE.NEXTVAL AS ID_VOLANTE FROM DUAL")
        new_id = seq_result[0]['ID_VOLANTE']
        
        query = """
            INSERT INTO VOLANTE_MATRICULA 
            (ID_VOLANTE, ID_ESTUDIANTE, ID_PERIODO, ID_PROGRAMA, MODALIDAD, SEMESTRE_QUE_COBRA, 
             TIPO_GENERACION, FECHA_GENERACION)
            VALUES (:id, :id_est, :id_per, :id_prog, :mod, :sem, 'INDIVIDUAL', SYSDATE)
        """
        execute_update(query, {
            "id": new_id,
            "id_est": id_estudiante,
            "id_per": id_periodo,
            "id_prog": id_programa,
            "mod": modalidad,
            "sem": semestre_que_cobra
        })
        
        logger.info(f"✓ Volante individual creado: {new_id}")
        
        # Retornar el volante creado
        return get_volante_by_id(new_id)
    except Exception as e:
        logger.error(f"✗ Error al crear volante: {e}")
        raise


def create_volante_masiva(id_periodo: int, id_programa: int, modalidad: str, semestre_que_cobra: int) -> List[int]:
    """Crea volantes para todos los estudiantes del programa. 
    Retorna lista de IDs de volantes creados."""
    try:
        # Obtener todos los estudiantes del programa
        query_est = "SELECT ID_ESTUDIANTE FROM ESTUDIANTE WHERE ID_PROGRAMA = :id_prog ORDER BY ID_ESTUDIANTE"
        estudiantes = execute_query(query_est, {"id_prog": id_programa})
        
        if not estudiantes:
            logger.warning(f"⚠ No hay estudiantes en el programa {id_programa}")
            return []
        
        volantes_creados = []
        for est in estudiantes:
            try:
                volante = create_volante_individual(
                    est['ID_ESTUDIANTE'], 
                    id_periodo, 
                    id_programa, 
                    modalidad, 
                    semestre_que_cobra
                )
                if volante:
                    volantes_creados.append(volante['ID_VOLANTE'])
            except Exception as e:
                logger.warning(f"⚠ No se pudo crear volante para estudiante {est['ID_ESTUDIANTE']}: {e}")
                # Continuar con el siguiente estudiante
        
        logger.info(f"✓ Volantes masivos creados: {len(volantes_creados)} de {len(estudiantes)}")
        return volantes_creados
    except Exception as e:
        logger.error(f"✗ Error al crear volantes masivos: {e}")
        raise



