"""
services/cuenta_corriente.py — Consultas a vistas de Cuenta Corriente

Usa directamente las vistas de Oracle:
- VW_CUENTA_CORRIENTE_DETALLE → detalle línea por línea
- VW_SALDO_PERIODO → balance total por estudiante y periodo
"""

from app.services.database import execute_query
from typing import List, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def get_cuenta_corriente_detalle(id_estudiante: int) -> List[Dict[str, Any]]:
    """Obtiene el detalle completo de la cuenta corriente de un estudiante
    usando la vista VW_CUENTA_CORRIENTE_DETALLE."""
    try:
        query = """
            SELECT ID_ESTUDIANTE, CARNET, NOMBRE_COMPLETO, NOMBRE_PROGRAMA,
                   NOMBRE_PERIODO, ID_MOV, FECHA, CODIGO_DETALLE,
                   DESCRIPCION_MOVIMIENTO, GRUPO, DEBITO, CREDITO,
                   SALDO_ACUMULADO
            FROM VW_CUENTA_CORRIENTE_DETALLE
            WHERE ID_ESTUDIANTE = :id_est
            ORDER BY NOMBRE_PERIODO, FECHA, ID_MOV
        """
        results = execute_query(query, {"id_est": id_estudiante})
        for row in results:
            fecha = row.get("FECHA")
            if isinstance(fecha, datetime):
                row["FECHA"] = fecha.date()
        logger.info(f"✓ Cuenta corriente: {len(results)} movimientos para estudiante {id_estudiante}")
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener cuenta corriente: {e}")
        raise


def get_saldo_periodo(id_estudiante: int) -> List[Dict[str, Any]]:
    """Obtiene el saldo por periodo de un estudiante
    usando la vista VW_SALDO_PERIODO."""
    try:
        query = """
            SELECT ID_ESTUDIANTE, ESTUDIANTE, ID_PERIODO, NOMBRE_PERIODO,
                   TOTAL_COBROS, TOTAL_PAGOS, SALDO_NETO
            FROM VW_SALDO_PERIODO
            WHERE ID_ESTUDIANTE = :id_est
            ORDER BY NOMBRE_PERIODO
        """
        results = execute_query(query, {"id_est": id_estudiante})
        logger.info(f"✓ Saldo periodo: {len(results)} periodos para estudiante {id_estudiante}")
        return results
    except Exception as e:
        logger.error(f"✗ Error al obtener saldo por periodo: {e}")
        raise
