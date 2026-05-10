r"""
test_db_direct.py — Test directo de queries SQL sin fastapi

Para debuggear exactamente qué falla
"""

import sys
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from app.services.database import execute_query, execute_update

print("\n" + "=" * 70)
print("TEST DE QUERIES DIRECTAS A BD")
print("=" * 70 + "\n")

try:
    # Test 1: Query simple sin parámetros
    print("🧪 Test 1: SELECT ID_PROGRAMA, NOMBRE_PROGRAMA FROM PROGRAMA_ACADEMICO")
    results = execute_query("SELECT ID_PROGRAMA, NOMBRE_PROGRAMA FROM PROGRAMA_ACADEMICO")
    print(f"   ✅ Resultado: {len(results)} filas encontradas")
    for row in results[:3]:
        print(f"      {row}")
    
    # Test 2: Query con parámetro nombrado
    print("\n🧪 Test 2: SELECT con parámetro nombrado (:id)")
    query = "SELECT ID_PROGRAMA, NOMBRE_PROGRAMA FROM PROGRAMA_ACADEMICO WHERE ID_PROGRAMA = :id"
    results = execute_query(query, {"id": 1})
    print(f"   ✅ Resultado: {len(results)} filas encontradas")
    for row in results:
        print(f"      {row}")
    
    # Test 3: Query con ORDER BY DESC
    print("\n🧪 Test 3: SELECT con ORDER BY DESC FETCH FIRST 1")
    query = "SELECT ID_PROGRAMA, NOMBRE_PROGRAMA FROM PROGRAMA_ACADEMICO ORDER BY ID_PROGRAMA DESC FETCH FIRST 1 ROW ONLY"
    results = execute_query(query)
    print(f"   ✅ Resultado: {len(results)} fila(s) encontrada(s)")
    for row in results:
        print(f"      {row}")
    
    print("\n" + "=" * 70)
    print("✅ TODOS LOS TESTS PASARON")
    print("=" * 70 + "\n")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)
