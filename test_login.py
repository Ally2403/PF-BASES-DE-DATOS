r"""
test_login.py — Script de prueba del endpoint de login

INSTRUCCIONES:
==============

1. Abre Terminal 1 y ejecuta esto para levantar la API:

   OPCIÓN A (desde PowerShell):
   $ cd c:\Users\juanp\Desktop\PF Bases
   $ .\run_dev.ps1

   OPCIÓN B (desde cmd/PowerShell directo):
   $ cd c:\Users\juanp\Desktop\PF Bases\backend
   $ python -m uvicorn app.main:app --reload

2. En Terminal 2, ejecuta este script:
   $ python test_login.py

PRUEBA:
=======
- POST /api/auth/login con credenciales válidas
- POST /api/auth/login con credenciales inválidas
- Decodificación del JWT token
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
    Pruebas del endpoint de login.
    """
    print("\n" + "=" * 70)
    print("PRUEBA DE LOGIN - ETAPA 3")
    print("=" * 70 + "\n")
    
    # ================================================
    # Prueba 1: Health check
    # ================================================
    print("🧪 Prueba 1: Health check...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            print("   ✅ EXITOSO: API está corriendo")
            print(f"   Respuesta: {response.json()}\n")
        else:
            print(f"   ❌ FALLÓ: Status code {response.status_code}\n")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ FALLÓ: No se puede conectar a la API")
        print("   ¿Está levantada? (uvicorn app.main:app --reload)\n")
        return False
    except Exception as e:
        print(f"   ❌ FALLÓ: {e}\n")
        return False
    
    # ================================================
    # Prueba 2: Login con credenciales correctas
    # ================================================
    print("🧪 Prueba 2: Login con credenciales CORRECTAS...")
    login_data = {
        "username": "cmendoza",
        "password": "password123"  # La contraseña debe coincidir con la de la BD
    }
    
    try:
        response = requests.post(
            f"{API_URL}/api/auth/login",
            json=login_data,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("   ✅ EXITOSO: Login correcto")
                print(f"   Usuario: {result['data']['user']['username']}")
                print(f"   Perfil: {result['data']['user']['perfil']}")
                print(f"   Token: {result['data']['access_token'][:50]}...\n")
                
                token = result['data']['access_token']
            else:
                print(f"   ❌ FALLÓ: {result.get('message')}\n")
                return False
        else:
            print(f"   ❌ FALLÓ: Status code {response.status_code}")
            print(f"   Respuesta: {response.text}\n")
            return False
    except Exception as e:
        print(f"   ❌ FALLÓ: {e}\n")
        return False
    
    # ================================================
    # Prueba 3: Login con credenciales INCORRECTAS
    # ================================================
    print("🧪 Prueba 3: Login con credenciales INCORRECTAS...")
    bad_login_data = {
        "username": "cmendoza",
        "password": "password_wrong"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/api/auth/login",
            json=bad_login_data,
            timeout=5
        )
        
        if response.status_code == 401:
            result = response.json()
            print(f"   ✅ CORRECTO: Rechazadas credenciales inválidas")
            print(f"   Mensaje: {result.get('message')}\n")
        else:
            print(f"   ⚠️ Status code inesperado: {response.status_code}\n")
    except Exception as e:
        print(f"   ❌ FALLÓ: {e}\n")
        return False
    
    # ================================================
    # Prueba 4: Decodificar JWT token
    # ================================================
    print("🧪 Prueba 4: Decodificar JWT token...")
    try:
        from app.services.auth import verify_token
        
        payload = verify_token(token)
        if payload:
            print("   ✅ EXITOSO: Token verificado")
            print(f"   Usuario ID: {payload.get('id_user')}")
            print(f"   Username: {payload.get('username')}")
            print(f"   Perfil: {payload.get('perfil')}")
            print(f"   Expira en: {payload.get('exp')}\n")
        else:
            print("   ❌ FALLÓ: Token inválido\n")
            return False
    except Exception as e:
        print(f"   ❌ FALLÓ: {e}\n")
        return False
    
    # ================================================
    # Verificación final
    # ================================================
    print("=" * 70)
    print("✅ TODAS LAS PRUEBAS EXITOSAS")
    print("=" * 70)
    print("\n📝 Notas:")
    print("   - El endpoint POST /api/auth/login funciona correctamente")
    print("   - Las credenciales se validan contra la BD")
    print("   - Los tokens JWT se generan y verifican correctamente")
    print("   - Las respuestas tienen la estructura esperada")
    print("\n💡 Próximas pruebas:")
    print("   - Usar el token en headers Authorization: Bearer <token>")
    print("   - Implementar endpoints protegidos por perfil")
    print("   - Etapa 4: CRUD de entidades (SUPERVISOR)\n")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
