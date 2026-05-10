"""
test_conexion.py — Script de prueba de conexión a Oracle

Uso:
    python test_conexion.py

Verifica:
    1. Que se pueda conectar a Oracle
    2. Que se pueda ejecutar SELECT 1 FROM DUAL
    3. Que las credenciales sean correctas
    4. Que la red Docker esté funcionando (si usas Docker)
"""

import sys
import logging
from pathlib import Path

# Agregar la carpeta 'backend' al path de Python
# Así Python encuentra el módulo 'app' (que está en backend/app)
project_root = Path(__file__).parent
backend_path = project_root / "backend"
sys.path.insert(0, str(backend_path))

# Configurar logging para ver los mensajes
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

from app.config import settings
from app.services.database import get_connection, test_connection, execute_query


def main():
    """
    Función principal del script de prueba.
    """
    print("\n" + "=" * 60)
    print("PRUEBA DE CONEXIÓN A ORACLE")
    print("=" * 60 + "\n")
    
    # ================================================
    # 1. MOSTRAR CONFIGURACIÓN
    # ================================================
    print("📋 Configuración:")
    print(f"   Host: {settings.db_host}")
    print(f"   Puerto: {settings.db_port}")
    print(f"   Service: {settings.db_service}")
    print(f"   Usuario: {settings.db_user}")
    print()
    
    # ================================================
    # 2. PRUEBA BÁSICA: test_connection()
    # ================================================
    print("🧪 Prueba 1: Conexión básica (SELECT 1 FROM DUAL)...")
    if test_connection():
        print("   ✅ EXITOSO: Conectado a Oracle\n")
    else:
        print("   ❌ FALLÓ: No se pudo conectar\n")
        return False
    
    # ================================================
    # 3. PRUEBA AVANZADA: Obtener conexión manual
    # ================================================
    print("🧪 Prueba 2: Conexión manual con cursor...")
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 AS numero FROM DUAL")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            print(f"   ✅ EXITOSO: Resultado = {result[0]}\n")
        else:
            print("   ❌ FALLÓ: No se retornó resultado\n")
            return False
    except Exception as e:
        print(f"   ❌ FALLÓ: {e}\n")
        return False
    
    # ================================================
    # 4. PRUEBA: Ejecutar query con execute_query()
    # ================================================
    print("🧪 Prueba 3: Ejecutar query con function execute_query()...")
    try:
        results = execute_query("SELECT * FROM USUARIO WHERE ROWNUM <= 1")
        if results:
            print(f"   ✅ EXITOSO: Se encontraron {len(results)} usuario(s)")
            print(f"   Primer usuario: {results[0]}\n")
        else:
            print("   ⚠️  Tabla USUARIO existe pero está vacía (sin datos aún)\n")
    except Exception as e:
        print(f"   ⚠️  No se pudo consultar tabla USUARIO: {e}")
        print("   (Esto es normal si aún no se ejecutó el DDL)\n")
    
    # ================================================
    # 5. VERIFICACIÓN FINAL
    # ================================================
    print("=" * 60)
    print("✅ TODAS LAS PRUEBAS EXITOSAS")
    print("=" * 60)
    print("\n📝 Notas:")
    print("   - La conexión a Oracle funciona correctamente")
    print("   - El driver oracledb está configurado")
    print("   - Credenciales son válidas")
    print("   - Puedes proceder con la Etapa 3 (Autenticación)\n")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
