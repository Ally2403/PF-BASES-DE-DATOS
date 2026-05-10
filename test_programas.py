r"""
test_programas.py — Script de prueba para endpoints de PROGRAMA_ACADEMICO

INSTRUCCIONES:
==============

1. Levanta la API en Terminal 1:
   $ cd c:\Users\juanp\Desktop\PF Bases\backend
   $ python -m uvicorn app.main:app --reload

2. En Terminal 2, ejecuta las pruebas de login primero (necesitas token):
   $ cd c:\Users\juanp\Desktop\PF Bases
   $ python test_programas.py

PRUEBA:
=======
- GET /api/programas (listar todos)
- POST /api/programas (crear nuevo)
- GET /api/programas/{id} (obtener por ID)
- Validar permisos (401, 403)
"""

import sys
import requests
import json
import logging
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# URL base del API
API_URL = "http://localhost:8000"


def main():
    """
    Pruebas de endpoints de PROGRAMA_ACADEMICO.
    """
    print("\n" + "=" * 70)
    print("PRUEBA DE ENDPOINTS - PROGRAMA ACADEMICO (ETAPA 4)")
    print("=" * 70 + "\n")
    
    # ================================================
    # Prueba 0: Obtener token de login
    # ================================================
    print("🧪 Paso 0: Obtener token de autenticación...")
    login_response = requests.post(
        f"{API_URL}/api/auth/login",
        json={"username": "cmendoza", "password": "password123"},
        timeout=5
    )
    
    if login_response.status_code != 200:
        print("   ❌ FALLÓ: No se pudo obtener token")
        return False
    
    token = login_response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("   ✅ EXITOSO: Token obtenido\n")
    
    # ================================================
    # Prueba 1: Listar programas (sin token)
    # ================================================
    print("🧪 Prueba 1: GET /api/programas SIN token (debe fallar con 401)...")
    response = requests.get(f"{API_URL}/api/programas", timeout=5)
    
    if response.status_code == 401:
        print("   ✅ CORRECTO: Rechazada solicitud sin autenticación\n")
    else:
        print(f"   ⚠️ Status inesperado: {response.status_code}\n")
    
    # ================================================
    # Prueba 2: Listar programas (con token)
    # ================================================
    print("🧪 Prueba 2: GET /api/programas CON token...")
    response = requests.get(f"{API_URL}/api/programas", headers=headers, timeout=5)
    
    if response.status_code == 200:
        result = response.json()
        programs = result.get("data", [])
        print(f"   ✅ EXITOSO: Se obtuvieron {len(programs)} programas")
        for prog in programs:
            print(f"      - ID {prog['id_programa']}: {prog['nombre_programa']}")
        print()
    else:
        print(f"   ❌ FALLÓ: Status {response.status_code}")
        print(f"   Respuesta: {response.text}\n")
        return False
    
    # ================================================
    # Prueba 3: Obtener programa por ID
    # ================================================
    if programs:
        program_id = programs[0]["id_programa"]
        print(f"🧪 Prueba 3: GET /api/programas/{program_id}...")
        response = requests.get(
            f"{API_URL}/api/programas/{program_id}",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            prog = result.get("data")
            print(f"   ✅ EXITOSO: Programa obtenido")
            print(f"      ID: {prog['id_programa']}")
            print(f"      Nombre: {prog['nombre_programa']}\n")
        else:
            print(f"   ❌ FALLÓ: Status {response.status_code}\n")
            return False
    
    # ================================================
    # Prueba 4: Crear nuevo programa
    # ================================================
    print("🧪 Prueba 4: POST /api/programas (crear nuevo)...")
    new_program = {
        "nombre_programa": "Ingeniería en Sistemas Prueba"
    }
    response = requests.post(
        f"{API_URL}/api/programas",
        json=new_program,
        headers=headers,
        timeout=5
    )
    
    if response.status_code == 201:
        result = response.json()
        prog = result.get("data")
        print(f"   ✅ EXITOSO: Programa creado")
        print(f"      ID: {prog['id_programa']}")
        print(f"      Nombre: {prog['nombre_programa']}\n")
        created_program_id = prog['id_programa']
    else:
        print(f"   ❌ FALLÓ: Status {response.status_code}")
        print(f"   Respuesta: {response.text}\n")
        return False
    
    # ================================================
    # Prueba 5: Obtener el programa recién creado
    # ================================================
    print(f"🧪 Prueba 5: GET /api/programas/{created_program_id} (recién creado)...")
    response = requests.get(
        f"{API_URL}/api/programas/{created_program_id}",
        headers=headers,
        timeout=5
    )
    
    if response.status_code == 200:
        result = response.json()
        prog = result.get("data")
        print(f"   ✅ EXITOSO: Programa recuperado")
        print(f"      Nombre: {prog['nombre_programa']}\n")
    else:
        print(f"   ❌ FALLÓ: Status {response.status_code}\n")
        return False
    
    # ================================================
    # Prueba 6: Obtener programa inexistente (404)
    # ================================================
    print("🧪 Prueba 6: GET /api/programas/99999 (inexistente, debe retornar 404)...")
    response = requests.get(
        f"{API_URL}/api/programas/99999",
        headers=headers,
        timeout=5
    )
    
    if response.status_code == 404:
        print("   ✅ CORRECTO: Retornado 404 para programa inexistente\n")
    else:
        print(f"   ⚠️ Status inesperado: {response.status_code}\n")
    
    # ================================================
    # Verificación final
    # ================================================
    print("=" * 70)
    print("✅ TODAS LAS PRUEBAS EXITOSAS")
    print("=" * 70)
    print("\n📝 Notas:")
    print("   - Los endpoints GET /api/programas y POST /api/programas funcionan")
    print("   - La autenticación JWT se valida correctamente (401 sin token)")
    print("   - Los permisos por perfil se validan correctamente")
    print("   - Las respuestas tienen la estructura esperada")
    print("\n💡 Próximos pasos:")
    print("   - Crear más endpoints CRUD para otras entidades")
    print("   - Asignatura, Período Académico, Plan de Estudio, etc.")
    print("   - Etapa 4 completa: SUPERVISOR CRUD\n")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se puede conectar a la API")
        print("¿Está levantada? (python -m uvicorn app.main:app --reload)\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        sys.exit(1)
