"""
test_administrador.py — Tests para endpoints de ADMINISTRADOR (Etapa 5)
"""

import requests
import time

BASE_URL = "http://localhost:8000/api"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def headers_with_auth():
    """Obtener headers con token JWT."""
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
    )
    token = login_response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def login():
    """Probar login como ADMINISTRADOR."""
    print("\n[*] Autenticando como ADMINISTRADOR...")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
    )
    
    if response.status_code != 200:
        print(f"[FAIL] Login failed: {response.text}")
        raise AssertionError(f"Login failed: {response.text}")
    
    data = response.json()
    token = data["data"]["access_token"]
    print(f"[OK] Token obtenido: {token[:30]}...")
    return token


def test_personas():
    """Test PERSONA CRUD."""
    print("\n" + "="*60)
    print("TEST 1: PERSONA CRUD (ADMINISTRADOR)")
    print("="*60)
    
    # GET /personas
    response = requests.get(
        f"{BASE_URL}/personas",
        headers=headers_with_auth()
    )
    assert response.status_code == 200
    personas_count = len(response.json()["data"])
    print(f"  [OK] GET /personas -> {personas_count} personas")
    
    # POST /personas
    unique_cedula = 1000000000 + int(time.time() % 1000000)
    response = requests.post(
        f"{BASE_URL}/personas",
        json={
            "cedula": unique_cedula,
            "nombre": "Carlos",
            "apellido": f"Admin{int(time.time())}",
            "correo": f"admin{int(time.time())}@test.com",
            "telefono": "3001234567"
        },
        headers=headers_with_auth()
    )
    
    if response.status_code != 201:
        print(f"  [ERROR] POST /personas returned {response.status_code}")
        print(f"  Response: {response.text}")
        raise AssertionError(f"Failed to create persona: {response.text}")
    
    new_cedula = response.json()["data"]["cedula"]
    print(f"  [OK] POST /personas -> Cédula {new_cedula} creada")
    
    # GET /personas/{cedula}
    response = requests.get(
        f"{BASE_URL}/personas/{new_cedula}",
        headers=headers_with_auth()
    )
    assert response.status_code == 200
    print(f"  [OK] GET /personas/{new_cedula} -> Verificada")


def test_usuarios():
    """Test USUARIO CRUD."""
    print("\n" + "="*60)
    print("TEST 2: USUARIO CRUD (ADMINISTRADOR)")
    print("="*60)
    
    # GET /usuarios
    response = requests.get(
        f"{BASE_URL}/usuarios",
        headers=headers_with_auth()
    )
    assert response.status_code == 200
    usuarios_count = len(response.json()["data"])
    print(f"  [OK] GET /usuarios -> {usuarios_count} usuarios")
    
    # Crear persona primero (para el FK)
    unique_cedula = 1000000000 + int(time.time() % 1000000)
    requests.post(
        f"{BASE_URL}/personas",
        json={
            "cedula": unique_cedula,
            "nombre": "Test",
            "apellido": "User",
            "correo": f"testuser{int(time.time())}@test.com",
            "telefono": "3009999999"
        },
        headers=headers_with_auth()
    )
    
    # POST /usuarios
    unique_username = f"testuser{int(time.time())}"
    response = requests.post(
        f"{BASE_URL}/usuarios",
        json={
            "username": unique_username,
            "contrasena": "password123",
            "id_perfil": 1,  # Asumiendo que existe ID_PERFIL = 1
            "cedula": unique_cedula
        },
        headers=headers_with_auth()
    )
    
    if response.status_code != 201:
        print(f"  [ERROR] POST /usuarios returned {response.status_code}")
        print(f"  Response: {response.text}")
        raise AssertionError(f"Failed to create usuario: {response.text}")
    
    new_id = response.json()["data"]["id_user"]
    print(f"  [OK] POST /usuarios -> ID {new_id} creado")
    
    # GET /usuarios/{id}
    response = requests.get(
        f"{BASE_URL}/usuarios/{new_id}",
        headers=headers_with_auth()
    )
    assert response.status_code == 200
    print(f"  [OK] GET /usuarios/{new_id} -> Verificado")


def test_perfiles():
    """Test PERFIL CRUD."""
    print("\n" + "="*60)
    print("TEST 3: PERFIL CRUD (ADMINISTRADOR)")
    print("="*60)
    
    # GET /perfiles
    response = requests.get(
        f"{BASE_URL}/perfiles",
        headers=headers_with_auth()
    )
    assert response.status_code == 200
    perfiles_count = len(response.json()["data"])
    print(f"  [OK] GET /perfiles -> {perfiles_count} perfiles")
    
    # POST /perfiles
    unique_name = f"TestPerfil{int(time.time())}"
    response = requests.post(
        f"{BASE_URL}/perfiles",
        json={"nombre_perfil": unique_name},
        headers=headers_with_auth()
    )
    
    if response.status_code != 201:
        print(f"  [ERROR] POST /perfiles returned {response.status_code}")
        print(f"  Response: {response.text}")
        raise AssertionError(f"Failed to create perfil: {response.text}")
    
    new_id = response.json()["data"]["id_perfil"]
    print(f"  [OK] POST /perfiles -> ID {new_id} creado: {unique_name}")
    
    # GET /perfiles/{id}
    response = requests.get(
        f"{BASE_URL}/perfiles/{new_id}",
        headers=headers_with_auth()
    )
    assert response.status_code == 200
    print(f"  [OK] GET /perfiles/{new_id} -> Verificado")


def test_menus():
    """Test MENU CRUD."""
    print("\n" + "="*60)
    print("TEST 4: MENU CRUD (ADMINISTRADOR)")
    print("="*60)
    
    # GET /menus
    response = requests.get(
        f"{BASE_URL}/menus",
        headers=headers_with_auth()
    )
    assert response.status_code == 200
    menus_count = len(response.json()["data"])
    print(f"  [OK] GET /menus -> {menus_count} menús")
    
    # POST /menus
    unique_name = f"TestMenu{int(time.time())}"
    response = requests.post(
        f"{BASE_URL}/menus",
        json={
            "nombre_funcion": unique_name,
            "url_acceso": "/test/menu"
        },
        headers=headers_with_auth()
    )
    
    if response.status_code != 201:
        print(f"  [ERROR] POST /menus returned {response.status_code}")
        print(f"  Response: {response.text}")
        raise AssertionError(f"Failed to create menu: {response.text}")
    
    new_id = response.json()["data"]["id_menu"]
    print(f"  [OK] POST /menus -> ID {new_id} creado: {unique_name}")
    
    # GET /menus/{id}
    response = requests.get(
        f"{BASE_URL}/menus/{new_id}",
        headers=headers_with_auth()
    )
    assert response.status_code == 200
    print(f"  [OK] GET /menus/{new_id} -> Verificado")


def main():
    """Ejecutar todos los tests."""
    print("\n" + "="*60)
    print("SUITE DE TESTS: ADMINISTRADOR (ETAPA 5)")
    print("="*60)
    
    try:
        login()
        test_personas()
        test_usuarios()
        test_perfiles()
        test_menus()
        
        print("\n" + "="*60)
        print("\n[OK] TODOS LOS TESTS PASARON")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n[FAIL] TEST FALLO: {e}")
        return False
    except Exception as e:
        print(f"\n[ERROR]: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
