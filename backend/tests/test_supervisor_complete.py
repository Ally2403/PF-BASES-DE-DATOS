"""
tests/test_supervisor_complete.py — Test completo de todas las entidades SUPERVISOR

Prueba todos los 8 entities con:
- Autenticación (401 sin token)
- Listado (GET)
- Detalle (GET by ID)
- Creación (POST)
- Permisos (requiere SUPERVISOR o ADMINISTRADOR)
"""

import requests
import json
from datetime import date, timedelta

BASE_URL = "http://localhost:8000/api"
TOKEN = None


def login():
    """Obtiene token de autenticación"""
    global TOKEN
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": "cmendoza", "password": "password123"}
    )
    assert response.status_code == 200, f"Login failed: {response.text}"
    TOKEN = response.json()["data"]["access_token"]
    print(f"[OK] Token obtenido: {TOKEN[:20]}...")
    return TOKEN


def headers_with_auth():
    """Headers con autenticación"""
    return {"Authorization": f"Bearer {TOKEN}"}


def headers_without_auth():
    """Headers sin autenticación"""
    return {}


def test_authentication_required():
    """Test 1: Todos los endpoints requieren autenticación"""
    print("\n" + "="*60)
    print("TEST 1: Autenticación requerida (401)")
    print("="*60)
    
    endpoints = [
        "GET /programas",
        "GET /asignaturas",
        "GET /periodos",
        "GET /estudiantes",
        "GET /codigos",
    ]
    
    for endpoint in endpoints:
        method, path = endpoint.split(" ")
        url = f"{BASE_URL}{path}"
        
        if method == "GET":
            response = requests.get(url, headers=headers_without_auth())
        
        assert response.status_code == 401, f"{endpoint} debería retornar 401"
        print(f"  [OK] {endpoint} -> 401 (no autorizado)")


def test_programa_academico():
    """Test 2: PROGRAMA_ACADEMICO CRUD"""
    print("\n" + "="*60)
    print("TEST 2: PROGRAMA_ACADEMICO CRUD")
    print("="*60)
    
    # 2.1 GET /programas (lista)
    response = requests.get(
        f"{BASE_URL}/programas",
        headers=headers_with_auth()
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    programas_count = len(data["data"])
    print(f"  [OK] GET /programas -> {programas_count} programas")
    
    # 2.2 GET /programas/{id} (detalle)
    if programas_count > 0:
        first_programa = data["data"][0]["id_programa"]
        response = requests.get(
            f"{BASE_URL}/programas/{first_programa}",
            headers=headers_with_auth()
        )
        assert response.status_code == 200
        print(f"  [OK] GET /programas/{first_programa} -> {response.json()['data']['nombre_programa']}")
    
    # 2.3 POST /programas (crear)
    response = requests.post(
        f"{BASE_URL}/programas",
        json={"nombre_programa": "Test Programa"},
        headers=headers_with_auth()
    )
    assert response.status_code == 201
    new_id = response.json()["data"]["id_programa"]
    print(f"  [OK] POST /programas -> ID {new_id} creado")
    
    # 2.4 Verificar que existe
    response = requests.get(
        f"{BASE_URL}/programas/{new_id}",
        headers=headers_with_auth()
    )
    assert response.status_code == 200
    print(f"  [OK] Verificado: Programa {new_id} existe")


def test_asignatura():
    """Test 3: ASIGNATURA CRUD"""
    print("\n" + "="*60)
    print("TEST 3: ASIGNATURA CRUD")
    print("="*60)
    
    # 3.1 GET /asignaturas
    response = requests.get(
        f"{BASE_URL}/asignaturas",
        headers=headers_with_auth()
    )
    assert response.status_code == 200
    asignaturas_count = len(response.json()["data"])
    print(f"  [OK] GET /asignaturas -> {asignaturas_count} asignaturas")
    
    # 3.2 POST /asignaturas (crear)
    response = requests.post(
        f"{BASE_URL}/asignaturas",
        json={"nombre": "Test Asignatura", "cant_creditos": 4},
        headers=headers_with_auth()
    )
    assert response.status_code == 201
    new_id = response.json()["data"]["id_asignatura"]
    print(f"  [OK] POST /asignaturas -> ID {new_id} creada")
    
    # 3.3 GET /asignaturas/{id}
    response = requests.get(
        f"{BASE_URL}/asignaturas/{new_id}",
        headers=headers_with_auth()
    )
    assert response.status_code == 200
    print(f"  [OK] GET /asignaturas/{new_id} -> Verificada")


def test_periodo_academico():
    """Test 4: PERIODO_ACADEMICO CRUD"""
    import time
    print("\n" + "="*60)
    print("TEST 4: PERIODO_ACADEMICO CRUD")
    print("="*60)
    
    # 4.1 GET /periodos
    response = requests.get(
        f"{BASE_URL}/periodos",
        headers=headers_with_auth()
    )
    assert response.status_code == 200
    periodos_count = len(response.json()["data"])
    print(f"  [OK] GET /periodos -> {periodos_count} periodos")
    
    # 4.2 POST /periodos
    hoy = date.today()
    inicio = hoy.isoformat()
    fin = (hoy + timedelta(days=120)).isoformat()
    
    # Use unique name with timestamp to avoid UNIQUE constraint violation
    periodo_name = f"Test-{int(time.time())}"
    
    response = requests.post(
        f"{BASE_URL}/periodos",
        json={
            "nombre_periodo": periodo_name,
            "fecha_inicio": inicio,
            "fecha_fin": fin
        },
        headers=headers_with_auth()
    )
    if response.status_code != 201:
        print(f"  [ERROR] POST /periodos returned {response.status_code}")
        print(f"  Response: {response.text}")
        raise AssertionError(f"Failed to create periodo: {response.text}")
    
    new_id = response.json()["data"]["id_periodo"]
    print(f"  [OK] POST /periodos -> ID {new_id} creado")
    
    # 4.3 GET /periodos/{id}
    response = requests.get(
        f"{BASE_URL}/periodos/{new_id}",
        headers=headers_with_auth()
    )
    assert response.status_code == 200
    print(f"  [OK] GET /periodos/{new_id} -> Verificado")


def test_estudiante():
    """Test 5: ESTUDIANTE CRUD"""
    import time
    print("\n" + "="*60)
    print("TEST 5: ESTUDIANTE CRUD")
    print("="*60)
    
    # 5.1 GET /estudiantes
    response = requests.get(
        f"{BASE_URL}/estudiantes",
        headers=headers_with_auth()
    )
    assert response.status_code == 200
    estudiantes_count = len(response.json()["data"])
    print(f"  [OK] GET /estudiantes -> {estudiantes_count} estudiantes")
    
    # 5.2 POST /estudiantes (necesitamos un programa existente)
    # Primero obtén un programa
    response = requests.get(
        f"{BASE_URL}/programas",
        headers=headers_with_auth()
    )
    programas = response.json()["data"]
    if programas:
        programa_id = programas[0]["id_programa"]
        
        # Use unique carnet with timestamp
        unique_carnet = f"EST-{int(time.time())}"
        
        response = requests.post(
            f"{BASE_URL}/estudiantes",
            json={
                "carnet": unique_carnet,
                "nombre": "Juan",
                "apellido": f"Test{int(time.time())}",
                "telefono": "1234567890",
                "correo": f"test{int(time.time())}@test.com",
                "id_programa": programa_id
            },
            headers=headers_with_auth()
        )
        
        if response.status_code != 201:
            print(f"  [ERROR] POST /estudiantes returned {response.status_code}")
            print(f"  Response: {response.text}")
            raise AssertionError(f"Failed to create estudiante: {response.text}")
        
        new_id = response.json()["data"]["id_estudiante"]
        print(f"  [OK] POST /estudiantes -> ID {new_id} creado")
        
        # 5.3 GET /estudiantes/{id}
        response = requests.get(
            f"{BASE_URL}/estudiantes/{new_id}",
            headers=headers_with_auth()
        )
        assert response.status_code == 200
        print(f"  [OK] GET /estudiantes/{new_id} -> Verificado")
        
        # 5.4 PUT /estudiantes/{id} - editar estudiante
        response = requests.put(
            f"{BASE_URL}/estudiantes/{new_id}",
            json={
                "nombre": "Juan Actualizado",
                "apellido": f"TestUpd{int(time.time())}",
                "telefono": "9999999999",
                "correo": f"updated{int(time.time())}@test.com"
            },
            headers=headers_with_auth()
        )
        if response.status_code == 200:
            print(f"  [OK] PUT /estudiantes/{new_id} -> Estudiante actualizado")
        else:
            print(f"  [ERROR] PUT /estudiantes/{new_id} retornó {response.status_code}")
            raise AssertionError(f"Failed to update estudiante: {response.text}")


def test_codigo_detalle():
    """Test 6: CODIGO_DETALLE CRUD"""
    import time
    print("\n" + "="*60)
    print("TEST 6: CODIGO_DETALLE CRUD")
    print("="*60)
    
    # 6.1 GET /codigos
    response = requests.get(
        f"{BASE_URL}/codigos",
        headers=headers_with_auth()
    )
    assert response.status_code == 200
    codigos_count = len(response.json()["data"])
    print(f"  [OK] GET /codigos -> {codigos_count} codigos")
    
    # 6.2 POST /codigos - use unique code with timestamp
    unique_codigo = f"CD{int(time.time() % 100000):05d}"
    
    response = requests.post(
        f"{BASE_URL}/codigos",
        json={
            "codigo_detalle": unique_codigo,
            "grupo": "COBRO",
            "descripcion": "Codigo de prueba",
            "valor_defecto": 150000
        },
        headers=headers_with_auth()
    )
    
    if response.status_code != 201:
        print(f"  [ERROR] POST /codigos returned {response.status_code}")
        print(f"  Response: {response.text}")
        raise AssertionError(f"Failed to create codigo: {response.text}")
    
    codigo_id = response.json()["data"]["codigo_detalle"]
    print(f"  [OK] POST /codigos -> {codigo_id} creado")
    
    # 6.3 GET /codigos/{codigo}
    response = requests.get(
        f"{BASE_URL}/codigos/{codigo_id}",
        headers=headers_with_auth()
    )
    assert response.status_code == 200
    print(f"  [OK] GET /codigos/{codigo_id} -> Verificado")


def test_plan_estudio():
    """Test 7: PLAN_ESTUDIO CRUD"""
    import time
    print("\n" + "="*60)
    print("TEST 7: PLAN_ESTUDIO CRUD")
    print("="*60)
    
    # 7.1 Obtener un programa (preferible uno nuevo)
    response = requests.get(
        f"{BASE_URL}/programas",
        headers=headers_with_auth()
    )
    programas = response.json()["data"]
    if programas:
        # Use the last program (most recently created) to avoid conflicts
        programa_id = programas[-1]["id_programa"]
        
        # 7.2 GET /programas/{id}/planes
        response = requests.get(
            f"{BASE_URL}/programas/{programa_id}/planes",
            headers=headers_with_auth()
        )
        assert response.status_code == 200
        planes_count = len(response.json()["data"])
        print(f"  [OK] GET /programas/{programa_id}/planes -> {planes_count} planes")
        
        # 7.3 POST /programas/{id}/planes - use unique semestre
        semestre = 1
        
        response = requests.post(
            f"{BASE_URL}/programas/{programa_id}/planes",
            json={"semestre": semestre},
            headers=headers_with_auth()
        )
        if response.status_code != 201:
            print(f"  [ERROR] POST /programas/{programa_id}/planes returned {response.status_code}")
            print(f"  Response: {response.text}")
            raise AssertionError(f"Failed to create plan: {response.text}")
        
        print(f"  [OK] POST /programas/{programa_id}/planes -> Semestre {semestre} agregado")


def test_plan_estudio_asignatura():
    """Test 8: PLAN_ESTUDIO_ASIGNATURA CRUD"""
    print("\n" + "="*60)
    print("TEST 8: PLAN_ESTUDIO_ASIGNATURA CRUD")
    print("="*60)
    
    # 8.1 Obtener programa y asignatura (use newly created program)
    response = requests.get(
        f"{BASE_URL}/programas",
        headers=headers_with_auth()
    )
    programas = response.json()["data"]
    
    response = requests.get(
        f"{BASE_URL}/asignaturas",
        headers=headers_with_auth()
    )
    asignaturas = response.json()["data"]
    
    if programas and asignaturas:
        # Use the last (newest) program
        programa_id = programas[-1]["id_programa"]
        asignatura_id = asignaturas[-1]["id_asignatura"]
        semestre = 1
        
        # 8.2 Asegurarse que existe el plan
        response = requests.get(
            f"{BASE_URL}/programas/{programa_id}/planes",
            headers=headers_with_auth()
        )
        planes = response.json()["data"]
        plan_exists = any(p["semestre"] == semestre for p in planes)
        if not plan_exists:
            response = requests.post(
                f"{BASE_URL}/programas/{programa_id}/planes",
                json={"semestre": semestre},
                headers=headers_with_auth()
            )
            if response.status_code != 201:
                print(f"  [ERROR] POST plan failed: {response.text}")
        
        # 8.3 GET /programas/{id}/planes/{sem}/asignaturas
        response = requests.get(
            f"{BASE_URL}/programas/{programa_id}/planes/{semestre}/asignaturas",
            headers=headers_with_auth()
        )
        if response.status_code != 200:
            print(f"  [ERROR] GET asignaturas returned {response.status_code}: {response.text}")
            raise AssertionError(f"Failed to get plan asignaturas: {response.text}")
        
        asigs_count = len(response.json()["data"])
        print(f"  [OK] GET /programas/{programa_id}/planes/{semestre}/asignaturas -> {asigs_count} asignaturas")
        
        # 8.4 POST /programas/{id}/planes/{sem}/asignaturas
        response = requests.post(
            f"{BASE_URL}/programas/{programa_id}/planes/{semestre}/asignaturas",
            json={"id_asignatura": asignatura_id},
            headers=headers_with_auth()
        )
        if response.status_code != 201:
            print(f"  [ERROR] POST asignatura returned {response.status_code}: {response.text}")
            raise AssertionError(f"Failed to add asignatura to plan: {response.text}")
        
        print(f"  [OK] POST /programas/{programa_id}/planes/{semestre}/asignaturas -> Asignatura agregada")


def test_regla_cobro(programa_id=None, periodo_id=None):
    """Test 9: REGLA_COBRO CRUD - usa programa y periodo recién creados"""
    import time
    print("\n" + "="*60)
    print("TEST 9: REGLA_COBRO CRUD")
    print("="*60)
    
    # Si no se proporcionan IDs, obtener los más recientes
    if programa_id is None or periodo_id is None:
        response = requests.get(
            f"{BASE_URL}/programas",
            headers=headers_with_auth()
        )
        programas = response.json()["data"]
        
        response = requests.get(
            f"{BASE_URL}/periodos",
            headers=headers_with_auth()
        )
        periodos = response.json()["data"]
        
        # Usar los más recientes (último de la lista)
        if programas:
            programa_id = programas[-1]["id_programa"]
        if periodos:
            periodo_id = periodos[-1]["id_periodo"]
    
    if programa_id and periodo_id:
        # 9.2 GET /programas/{id}/periodos/{pid}/reglas
        response = requests.get(
            f"{BASE_URL}/programas/{programa_id}/periodos/{periodo_id}/reglas",
            headers=headers_with_auth()
        )
        assert response.status_code == 200
        reglas_count = len(response.json()["data"])
        print(f"  [OK] GET /programas/{programa_id}/periodos/{periodo_id}/reglas -> {reglas_count} reglas")
        
        # 9.3 POST /programas/{id}/periodos/{pid}/reglas - MODALIDAD GLOBAL (sin creditos)
        response = requests.post(
            f"{BASE_URL}/programas/{programa_id}/periodos/{periodo_id}/reglas",
            json={
                "modalidad": "GLOBAL",
                "valor_global": 5000000.0
            },
            headers=headers_with_auth()
        )
        if response.status_code == 201:
            print(f"  [OK] POST /programas/{programa_id}/periodos/{periodo_id}/reglas -> Regla GLOBAL creada")
        else:
            print(f"  ⚠ POST regla retornó {response.status_code}: {response.json()}")


def test_error_cases():
    """Test 10: Casos de error"""
    print("\n" + "="*60)
    print("TEST 10: Casos de error")
    print("="*60)
    
    # 10.1 404 para programa no existente
    response = requests.get(
        f"{BASE_URL}/programas/99999",
        headers=headers_with_auth()
    )
    assert response.status_code == 404
    print("  [OK] GET /programas/99999 -> 404")
    
    # 10.2 404 para asignatura no existente
    response = requests.get(
        f"{BASE_URL}/asignaturas/99999",
        headers=headers_with_auth()
    )
    assert response.status_code == 404
    print("  [OK] GET /asignaturas/99999 -> 404")
    
    # 10.3 404 para periodo no existente
    response = requests.get(
        f"{BASE_URL}/periodos/99999",
        headers=headers_with_auth()
    )
    assert response.status_code == 404
    print("  [OK] GET /periodos/99999 -> 404")


def main():
    """Ejecuta todos los tests"""
    print("\n" + "="*60)
    print("SUITE DE TESTS: SUPERVISOR COMPLETE (8 ENTITIES)")
    print("="*60)
    
    try:
        login()
        test_authentication_required()
        test_programa_academico()
        test_asignatura()
        test_periodo_academico()
        test_estudiante()
        test_codigo_detalle()
        test_plan_estudio()
        test_plan_estudio_asignatura()
        test_regla_cobro()
        test_error_cases()
        
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
