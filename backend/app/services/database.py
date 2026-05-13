"""
database.py — Módulo de conexión a Oracle usando oracledb
Este es el driver moderno de Oracle para Python (python-oracledb).

Provee:
- Función para obtener conexión
- Context manager para manejar conexiones
- Funciones auxiliares para ejecutar queries
"""

import oracledb
from typing import Optional, List, Dict, Any
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# =====================================================
# CONFIGURACION DE ORACLEDB
# =====================================================
# Modo thin: se conecta directamente sin Oracle Client instalado
# Más ligero, ideal para Docker
oracledb.init_oracle_client(lib_dir=None)  # None = usar thin mode


class OracleConnection:
    """
    Manejador de conexiones a Oracle.
    Usa context manager para garantizar que las conexiones se cierren.
    """
    
    def __init__(self):
        self.connection = None
    
    def __enter__(self):
        """Abre conexión al entrar al context."""
        try:
            self.connection = oracledb.connect(
                user=settings.db_user,
                password=settings.db_password,
                dsn=f"{settings.db_host}:{settings.db_port}/{settings.db_service}"
            )
            logger.info(f"✓ Conectado a Oracle: {settings.db_host}:{settings.db_port}/{settings.db_service}")
            return self.connection
        except oracledb.DatabaseError as e:
            logger.error(f"✗ Error de conexión a Oracle: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra conexión al salir del context."""
        if self.connection:
            self.connection.close()
            logger.info("✓ Conexión cerrada")


def get_connection() -> oracledb.Connection:
    """
    Obtiene una conexión a Oracle.
    
    Uso:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM DUAL")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
    
    Returns:
        oracledb.Connection: Conexión activa a Oracle
        
    Raises:
        oracledb.DatabaseError: Si no se puede conectar
    """
    try:
        conn = oracledb.connect(
            user=settings.db_user,
            password=settings.db_password,
            dsn=f"{settings.db_host}:{settings.db_port}/{settings.db_service}"
        )
        logger.info(f"✓ Conexión exitosa a Oracle")
        return conn
    except oracledb.DatabaseError as e:
        logger.error(f"✗ Error al conectar a Oracle: {e}")
        raise


def execute_query(query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
    """
    Ejecuta una query SELECT y retorna resultados como lista de diccionarios.
    
    Args:
        query: Query SQL (ej: "SELECT * FROM USUARIO WHERE ID_USER = :id")
        params: Parámetros para la query (tuple de valores)
    
    Returns:
        Lista de diccionarios con los resultados
        
    Example:
        results = execute_query("SELECT * FROM USUARIO WHERE ID_USER = :id", (1,))
        for row in results:
            print(row['USERNAME'], row['ID_USER'])
    """
    with OracleConnection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or {})
            
            # Obtener nombres de columnas
            column_names = [desc[0] for desc in cursor.description]
            
            # Convertir filas a diccionarios
            rows = cursor.fetchall()
            results = [dict(zip(column_names, row)) for row in rows]
            
            logger.info(f"✓ Query ejecutada: {len(results)} filas")
            return results
        except oracledb.DatabaseError as e:
            logger.error(f"✗ Error al ejecutar query: {e}")
            raise
        finally:
            cursor.close()


def execute_update(query: str, params: Optional[dict] = None) -> int:
    """
    Ejecuta un INSERT, UPDATE o DELETE y retorna número de filas afectadas.
    
    Args:
        query: Query SQL (ej: "INSERT INTO USUARIO (USERNAME, ...) VALUES (:username, ...)")
        params: Diccionario de parámetros nombrados
    
    Returns:
        Número de filas afectadas
        
    Example:
        affected = execute_update(
            "INSERT INTO USUARIO (USERNAME, CONTRASENA) VALUES (:username, :pwd)",
            {"username": "juan", "pwd": "hash123"}
        )
        print(f"Insertadas {affected} filas")
    """
    with OracleConnection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or {})
            conn.commit()
            rows_affected = cursor.rowcount
            logger.info(f"✓ Query ejecutada: {rows_affected} filas afectadas")
            return rows_affected
        except oracledb.DatabaseError as e:
            conn.rollback()
            logger.error(f"✗ Error al ejecutar update: {e}")
            raise
        finally:
            cursor.close()


def execute_procedure(procedure_name: str, params: Optional[list] = None) -> List[Any]:
    """
    Ejecuta un procedimiento almacenado de Oracle.
    
    Args:
        procedure_name: Nombre del procedimiento (ej: "PKG_USUARIOS.SP_CREAR_USUARIO")
        params: Parámetros posicionales para el procedimiento
    
    Returns:
        Resultados del procedimiento
        
    Example:
        result = execute_procedure("PKG_VOLANTES.SP_GENERAR_VOLANTE", [123, 1, "GLOBAL"])
    """
    with OracleConnection() as conn:
        cursor = conn.cursor()
        try:
            cursor.callproc(procedure_name, params or [])
            conn.commit()
            logger.info(f"✓ Procedimiento ejecutado: {procedure_name}")
            return cursor.fetchall() if hasattr(cursor, 'fetchall') else None
        except oracledb.DatabaseError as e:
            conn.rollback()
            logger.error(f"✗ Error al ejecutar procedimiento: {e}")
            raise
        finally:
            cursor.close()


def is_fk_violation(e: Exception) -> bool:
    """Detecta si una excepción es una violación de integridad referencial de Oracle (ORA-02292)."""
    msg = str(e)
    return "ORA-02292" in msg or ("integrity constraint" in msg.lower() and "violated" in msg.lower())


def execute_transaction(statements: list) -> None:
    """
    Ejecuta múltiples sentencias SQL en una sola transacción atómica.

    Args:
        statements: Lista de tuplas (query, params_dict). Si params_dict es None se usa {}.

    Raises:
        oracledb.DatabaseError: Si alguna sentencia falla (hace rollback de todas).
    """
    with OracleConnection() as conn:
        cursor = conn.cursor()
        try:
            for query, params in statements:
                cursor.execute(query, params or {})
            conn.commit()
            logger.info(f"✓ Transacción completada: {len(statements)} sentencias")
        except oracledb.DatabaseError as e:
            conn.rollback()
            logger.error(f"✗ Error en transacción, rollback ejecutado: {e}")
            raise
        finally:
            cursor.close()


def test_connection() -> bool:
    """
    Prueba la conexión a Oracle con un SELECT 1 FROM DUAL.
    
    Returns:
        True si la conexión es exitosa, False si falla
    """
    try:
        with OracleConnection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM DUAL")
            result = cursor.fetchone()
            cursor.close()
            return result is not None
    except Exception as e:
        logger.error(f"✗ Test de conexión fallido: {e}")
        return False
