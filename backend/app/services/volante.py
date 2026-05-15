"""
services/volante.py — Lógica de negocio para VOLANTE_MATRICULA
"""

from app.services.database import execute_query, execute_update
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def get_all_volantes(id_estudiante: Optional[int] = None, id_periodo: Optional[int] = None) -> List[Dict[str, Any]]:
    """Obtiene volantes. Si se pasan filtros, filtra por estudiante y/o periodo."""
    try:
        conditions = []
        params = {}
        if id_estudiante is not None:
            conditions.append("ID_ESTUDIANTE = :id_est")
            params["id_est"] = id_estudiante
        if id_periodo is not None:
            conditions.append("ID_PERIODO = :id_per")
            params["id_per"] = id_periodo
        where = (" WHERE " + " AND ".join(conditions)) if conditions else ""
        query = f"""
            SELECT ID_VOLANTE, SEMESTRE_QUE_COBRA, FECHA_GENERACION, 
                   TIPO_GENERACION, MONTO_TOTAL, ID_ESTUDIANTE, ID_PERIODO, MODALIDAD, ID_PROGRAMA
            FROM VOLANTE_MATRICULA{where} ORDER BY ID_VOLANTE DESC
        """
        results = execute_query(query, params if params else None)
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
                             modalidad: str, semestre_que_cobra: int,
                             asignaturas: Optional[List[int]] = None) -> Dict[str, Any]:
    """Crea un volante individual. El trigger TR_CALCULAR_MONTO_VOLANTE calcula el MONTO_TOTAL.
    Para modalidad CREDITOS, inserta asignaturas seleccionadas en VOLANTE_MATRICULA_ASIGNATURA."""
    try:
        # Obtener el siguiente ID
        seq_result = execute_query("SELECT SEQ_VOLANTE.NEXTVAL AS ID_VOLANTE FROM DUAL")
        new_id = seq_result[0]['ID_VOLANTE']
        
        query = """
            INSERT INTO VOLANTE_MATRICULA 
            (ID_VOLANTE, ID_ESTUDIANTE, ID_PERIODO, ID_PROGRAMA, MODALIDAD, SEMESTRE_QUE_COBRA, 
             TIPO_GENERACION, FECHA_GENERACION)
            VALUES (:id, :id_est, :id_per, :id_prog, :mod, :sem, 'INDIVIDUAL', :fecha_gen)
        """
        execute_update(query, {
            "id": new_id,
            "fecha_gen": datetime.now(),
            "id_est": id_estudiante,
            "id_per": id_periodo,
            "id_prog": id_programa,
            "mod": modalidad,
            "sem": semestre_que_cobra
        })
        
        # Para CREDITOS: insertar las asignaturas seleccionadas
        if modalidad == 'CREDITOS' and asignaturas:
            for id_asig in asignaturas:
                execute_update(
                    "INSERT INTO VOLANTE_MATRICULA_ASIGNATURA (ID_ASIGNATURA, ID_VOLANTE) VALUES (:asig, :vol)",
                    {"asig": id_asig, "vol": new_id}
                )
            logger.info(f"✓ {len(asignaturas)} asignaturas asociadas al volante {new_id}")

        # Obtener MONTO_TOTAL actualizado (puede haber sido recalculado por trigger)
        monto_result = execute_query(
            "SELECT MONTO_TOTAL FROM VOLANTE_MATRICULA WHERE ID_VOLANTE = :id",
            {"id": new_id}
        )
        monto_total = monto_result[0]['MONTO_TOTAL'] if monto_result else 0

        # Crear MOVIMIENTO de cobro en la CUENTA_CORRIENTE (creada por trigger)
        cc_result = execute_query(
            "SELECT ID_CUENTA FROM CUENTA_CORRIENTE WHERE ID_ESTUDIANTE = :id_est",
            {"id_est": id_estudiante}
        )
        if cc_result and monto_total:
            id_cuenta = cc_result[0]['ID_CUENTA']
            codigo_cobro = 'PCRE' if modalidad == 'CREDITOS' else 'PMAT'
            seq_mov = execute_query("SELECT SEQ_MOVIMIENTO.NEXTVAL AS ID_MOV FROM DUAL")
            new_mov_id = seq_mov[0]['ID_MOV']
            execute_update(
                """INSERT INTO MOVIMIENTO (ID_MOV, FECHA, VALOR, CODIGO_DETALLE, ID_VOLANTE, ID_PERIODO, ID_CUENTA)
                   VALUES (:id, :fecha, :valor, :cod, :id_vol, :id_per, :id_cta)""",
                {"id": new_mov_id, "fecha": datetime.now(), "valor": monto_total, "cod": codigo_cobro,
                 "id_vol": new_id, "id_per": id_periodo, "id_cta": id_cuenta}
            )
            logger.info(f"✓ Movimiento cobro {codigo_cobro} creado: id={new_mov_id}, valor={monto_total}")

        logger.info(f"✓ Volante individual creado: {new_id}")

        # Retornar el volante creado
        return get_volante_by_id(new_id)
    except Exception as e:
        logger.error(f"✗ Error al crear volante: {e}")
        raise


def create_volante_masiva(id_periodo: int, id_programa: int, modalidad: str, semestre_que_cobra: int) -> Dict[str, Any]:
    """Crea volantes para todos los estudiantes del programa.
    Retorna dict con creados, omitidos y lista de errores."""
    try:
        # Obtener todos los estudiantes del programa
        query_est = "SELECT ID_ESTUDIANTE FROM ESTUDIANTE WHERE ID_PROGRAMA = :id_prog ORDER BY ID_ESTUDIANTE"
        estudiantes = execute_query(query_est, {"id_prog": id_programa})
        
        if not estudiantes:
            logger.warning(f"⚠ No hay estudiantes en el programa {id_programa}")
            return {"creados": [], "errores": []}
        
        volantes_creados = []
        errores = []
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
                msg = str(e)
                logger.warning(f"⚠ No se pudo crear volante para estudiante {est['ID_ESTUDIANTE']}: {msg}")
                errores.append({"id_estudiante": est['ID_ESTUDIANTE'], "error": msg})
        
        logger.info(f"✓ Volantes masivos creados: {len(volantes_creados)} de {len(estudiantes)}")
        return {"creados": volantes_creados, "errores": errores}
    except Exception as e:
        logger.error(f"✗ Error al crear volantes masivos: {e}")
        raise



