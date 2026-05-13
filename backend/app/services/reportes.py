"""
services/reportes.py — Consultas a vistas de reportes (Etapa 8)

Usa directamente las vistas de Oracle (no duplica lógica de BD):
- VW_LISTADO_ESTUDIANTES
- VW_INGRESO_ESPERADO
- VW_PENDIENTES_PAGO
- VW_INGRESO_REAL
- VW_CARTERA
- VW_CONSULTA_PAGOS
"""

from app.services.database import execute_query
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def get_listado_estudiantes() -> List[Dict[str, Any]]:
    """Listado de estudiantes con programa, modalidad y monto.
    Vista: VW_LISTADO_ESTUDIANTES"""
    try:
        query = """
            SELECT le.ID_ESTUDIANTE, le.CARNET, le.NOMBRE_ESTUDIANTE, le.APELLIDO_ESTUDIANTE,
                   le.NOMBRE_PROGRAMA, le.NOMBRE_PERIODO, le.MODALIDAD, le.MONTO_TOTAL,
                   CASE
                       WHEN NVL(sp.SALDO_NETO, le.MONTO_TOTAL) <= 0 THEN 'PAGADO'
                       WHEN NVL(sp.TOTAL_PAGOS, 0) > 0             THEN 'PARCIAL'
                       ELSE 'PENDIENTE'
                   END AS ESTADO
            FROM VW_LISTADO_ESTUDIANTES le
            LEFT JOIN VW_SALDO_PERIODO sp
                   ON sp.ID_ESTUDIANTE  = le.ID_ESTUDIANTE
                  AND sp.NOMBRE_PERIODO = le.NOMBRE_PERIODO
            ORDER BY le.NOMBRE_PROGRAMA, le.NOMBRE_ESTUDIANTE
        """
        results = execute_query(query)
        logger.info(f"✓ Reporte listado estudiantes: {len(results)} registros")
        return results
    except Exception as e:
        logger.error(f"✗ Error en reporte listado estudiantes: {e}")
        raise


def get_ingreso_esperado() -> List[Dict[str, Any]]:
    """Ingreso esperado totalizado por periodo y programa.
    Vista: VW_INGRESO_ESPERADO"""
    try:
        query = """
            SELECT NOMBRE_PERIODO, NOMBRE_PROGRAMA, TOTAL_ESPERADO
            FROM VW_INGRESO_ESPERADO
            ORDER BY NOMBRE_PERIODO, NOMBRE_PROGRAMA
        """
        results = execute_query(query)
        logger.info(f"✓ Reporte ingreso esperado: {len(results)} registros")
        return results
    except Exception as e:
        logger.error(f"✗ Error en reporte ingreso esperado: {e}")
        raise


def get_pendientes_pago(id_programa: Optional[int] = None) -> List[Dict[str, Any]]:
    """Estudiantes pendientes de pago, filtrados opcionalmente por programa.
    Vista: VW_PENDIENTES_PAGO"""
    try:
        if id_programa:
            query = """
                SELECT ID_ESTUDIANTE, CARNET, NOMBRE_ESTUDIANTE, APELLIDO_ESTUDIANTE,
                       CORREO, TELEFONO, ID_PROGRAMA, NOMBRE_PROGRAMA, NOMBRE_PERIODO,
                       TOTAL_COBRADO, TOTAL_PAGADO, SALDO_PENDIENTE, ESTADO
                FROM VW_PENDIENTES_PAGO
                WHERE ID_PROGRAMA = :id_prog
                ORDER BY NOMBRE_ESTUDIANTE
            """
            results = execute_query(query, {"id_prog": id_programa})
        else:
            query = """
                SELECT ID_ESTUDIANTE, CARNET, NOMBRE_ESTUDIANTE, APELLIDO_ESTUDIANTE,
                       CORREO, TELEFONO, ID_PROGRAMA, NOMBRE_PROGRAMA, NOMBRE_PERIODO,
                       TOTAL_COBRADO, TOTAL_PAGADO, SALDO_PENDIENTE, ESTADO
                FROM VW_PENDIENTES_PAGO
                ORDER BY NOMBRE_PROGRAMA, NOMBRE_ESTUDIANTE
            """
            results = execute_query(query)

        logger.info(f"✓ Reporte pendientes pago: {len(results)} registros")
        return results
    except Exception as e:
        logger.error(f"✗ Error en reporte pendientes pago: {e}")
        raise


def get_ingreso_real() -> List[Dict[str, Any]]:
    """Ingreso real recibido por periodo.
    Vista: VW_INGRESO_REAL"""
    try:
        query = """
            SELECT NOMBRE_PERIODO, TOTAL_RECAUDADO
            FROM VW_INGRESO_REAL
            ORDER BY NOMBRE_PERIODO
        """
        results = execute_query(query)
        logger.info(f"✓ Reporte ingreso real: {len(results)} registros")
        return results
    except Exception as e:
        logger.error(f"✗ Error en reporte ingreso real: {e}")
        raise


def get_cartera() -> List[Dict[str, Any]]:
    """Estudiantes con crédito financiero (cartera / cuentas por cobrar).
    Vista: VW_CARTERA"""
    try:
        query = """
            SELECT ID_ESTUDIANTE, CARNET, NOMBRE_ESTUDIANTE, APELLIDO_ESTUDIANTE,
                   CORREO, NOMBRE_PROGRAMA, NOMBRE_PERIODO, VALOR_CREDITO
            FROM VW_CARTERA
            ORDER BY NOMBRE_PROGRAMA, NOMBRE_ESTUDIANTE
        """
        results = execute_query(query)
        logger.info(f"✓ Reporte cartera: {len(results)} registros")
        return results
    except Exception as e:
        logger.error(f"✗ Error en reporte cartera: {e}")
        raise


def get_consulta_pagos() -> List[Dict[str, Any]]:
    """Consulta consolidada de pagos (transacción + movimiento + estudiante).
    Vista: VW_CONSULTA_PAGOS"""
    try:
        query = """
            SELECT ID_TRANSACCION, REFERENCIA, MEDIO_PAGO, FECHA_PAGO,
                   VALOR_PAGADO, ID_MOV, CARNET, NOMBRE_ESTUDIANTE,
                   CONCEPTO, ID_PERIODO
            FROM VW_CONSULTA_PAGOS
            ORDER BY FECHA_PAGO DESC
        """
        results = execute_query(query)
        logger.info(f"✓ Reporte consulta pagos: {len(results)} registros")
        return results
    except Exception as e:
        logger.error(f"✗ Error en reporte consulta pagos: {e}")
        raise
