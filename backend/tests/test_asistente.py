"""
test_asistente.py — Suite de tests para endpoints ASISTENTE (cobros y pagos)
"""

import pytest
import requests
import time
import json
import sys

# =============================================
# CONFIGURACIÓN INICIAL
# =============================================
API_URL = "http://localhost:8000/api"
TIMEOUT = 10

# Credenciales de usuario ASISTENTE (ltorres del DDL semilla)
ASISTENTE_USER = "ltorres"
ASISTENTE_PASS = "password123"

# Token global
TOKEN = None


# =============================================
# FIXTURE: Obtener token de autenticación
# =============================================
@pytest.fixture(scope="session", autouse=True)
def setup_token():
    """Obtiene token de ASISTENTE al inicio de los tests."""
    global TOKEN
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            json={"username": ASISTENTE_USER, "password": ASISTENTE_PASS},
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            TOKEN = response.json()["data"]["access_token"]
            print(f"\n✓ Token ASISTENTE obtenido: {TOKEN[:20]}...")
        else:
            print(f"\n✗ No se pudo autenticar como ASISTENTE: {response.text}")
            raise Exception("No token")
    except Exception as e:
        print(f"\n✗ Error en setup: {e}")
        raise


def get_headers():
    """Retorna headers con autenticación."""
    return {"Authorization": f"Bearer {TOKEN}"}


# =============================================
# TESTS: OBTENER DATOS DE PRUEBA (ETAPAS 4 Y 5)
# =============================================

@pytest.mark.order(1)
def test_01_obtener_datos_prueba():
    """Obtiene IDs de PROGRAMA, PERIODO, ESTUDIANTE para crear volantes."""
    global PROGRAMA_ID, PERIODO_ID, ESTUDIANTE_ID

    try:
        # Obtener primer programa
        # supervisor usa prefix /api (sin /supervisor/)
        resp_prog = requests.get(f"{API_URL}/programas", headers=get_headers(), timeout=TIMEOUT)
        assert resp_prog.status_code == 200, f"Error obtener programas: {resp_prog.text}"
        programas = resp_prog.json()["data"]
        PROGRAMA_ID = programas[0]["id_programa"] if programas else None
        assert PROGRAMA_ID, "No hay programas disponibles"
        print(f"  ✓ PROGRAMA_ID: {PROGRAMA_ID}")

        # Obtener primer período
        resp_per = requests.get(f"{API_URL}/periodos", headers=get_headers(), timeout=TIMEOUT)
        assert resp_per.status_code == 200
        periodos = resp_per.json()["data"]
        PERIODO_ID = periodos[0]["id_periodo"] if periodos else None
        assert PERIODO_ID, "No hay períodos disponibles"
        print(f"  ✓ PERIODO_ID: {PERIODO_ID}")

        # Obtener primer estudiante
        resp_est = requests.get(f"{API_URL}/estudiantes", headers=get_headers(), timeout=TIMEOUT)
        assert resp_est.status_code == 200
        estudiantes = resp_est.json()["data"]
        ESTUDIANTE_ID = estudiantes[0]["id_estudiante"] if estudiantes else None
        assert ESTUDIANTE_ID, "No hay estudiantes disponibles"
        print(f"  ✓ ESTUDIANTE_ID: {ESTUDIANTE_ID}")

        # Verificar REGLA_COBRO para el programa/periodo
        resp_regla = requests.get(
            f"{API_URL}/programas/{PROGRAMA_ID}/periodos/{PERIODO_ID}/reglas",
            headers=get_headers(),
            timeout=TIMEOUT
        )
        if resp_regla.status_code == 200:
            reglas = resp_regla.json()["data"]
            if reglas:
                print(f"  ✓ Reglas de cobro encontradas: {len(reglas)}")
            else:
                print("  ⚠ No hay reglas de cobro para este programa/periodo")

        # Verificar PLAN_ESTUDIO
        resp_plan = requests.get(
            f"{API_URL}/programas/{PROGRAMA_ID}/planes",
            headers=get_headers(),
            timeout=TIMEOUT
        )
        if resp_plan.status_code == 200:
            planes = resp_plan.json()["data"]
            if planes:
                print(f"  ✓ Planes de estudio encontrados: {len(planes)}")

        assert PROGRAMA_ID and PERIODO_ID and ESTUDIANTE_ID, "Faltan datos críticos"
        print("✓ [OK] Datos de prueba obtenidos correctamente\n")

    except Exception as e:
        print(f"✗ [FAIL] Error: {e}\n")
        raise


# =============================================
# TESTS: VOLANTES INDIVIDUAL Y MASIVO
# =============================================

@pytest.mark.order(2)
def test_02_crear_volante_individual():
    """POST /volantes/individual — Crear volante para un estudiante."""
    global VOLANTE_ID

    try:
        payload = {
            "id_estudiante": ESTUDIANTE_ID,
            "id_periodo": PERIODO_ID,
            "id_programa": PROGRAMA_ID,
            "modalidad": "GLOBAL",
            "semestre_que_cobra": 1
        }

        response = requests.post(
            f"{API_URL}/asistente/volantes/individual",
            json=payload,
            headers=get_headers(),
            timeout=TIMEOUT
        )

        assert response.status_code == 200, f"Error: {response.text}"
        data = response.json()
        assert data["success"] is True
        assert "id_volante" in data["data"]

        VOLANTE_ID = data["data"]["id_volante"]
        print(f"  ✓ Volante individual creado: ID={VOLANTE_ID}")
        print(f"  ✓ Estado: {data['data']['estado']}")
        print(f"  ✓ Monto: ${data['data']['monto_total']}")
        print("✓ [OK] Volante individual creado correctamente\n")

    except Exception as e:
        print(f"✗ [FAIL] Error: {e}\n")
        raise


@pytest.mark.order(3)
def test_03_listar_volante():
    """GET /volantes/{id} — Obtener volante creado."""

    try:
        response = requests.get(
            f"{API_URL}/asistente/volantes/{VOLANTE_ID}",
            headers=get_headers(),
            timeout=TIMEOUT
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id_volante"] == VOLANTE_ID

        print(f"  ✓ Volante obtenido: {VOLANTE_ID}")
        print(f"  ✓ Estudiante: {data['data']['id_estudiante']}")
        print(f"  ✓ Período: {data['data']['id_periodo']}")
        print("✓ [OK] Volante obtenido correctamente\n")

    except Exception as e:
        print(f"✗ [FAIL] Error: {e}\n")
        raise


# =============================================
# TESTS: COBROS ADICIONALES
# =============================================

@pytest.mark.order(4)
def test_04_crear_cobro_adicional():
    """POST /cobros-adicionales — Agregar cobro adicional a volante."""

    try:
        monto_anterior = None

        # Obtener monto anterior
        resp_antes = requests.get(
            f"{API_URL}/asistente/volantes/{VOLANTE_ID}",
            headers=get_headers(),
            timeout=TIMEOUT
        )
        monto_anterior = resp_antes.json()["data"]["monto_total"]

        # Crear cobro adicional
        payload = {
            "id_volante": VOLANTE_ID,
            "codigo_detalle": "PLAB",
            "valor": 50000.0
        }

        response = requests.post(
            f"{API_URL}/asistente/cobros-adicionales",
            json=payload,
            headers=get_headers(),
            timeout=TIMEOUT
        )

        assert response.status_code == 200, f"Error: {response.text}"
        data = response.json()
        assert data["success"] is True

        monto_nuevo = data["data"]["monto_total"]
        print(f"  ✓ Cobro PLAB (${payload['valor']}) agregado")
        print(f"  ✓ Monto anterior: ${monto_anterior}")
        print(f"  ✓ Monto nuevo: ${monto_nuevo}")
        print("✓ [OK] Cobro adicional creado correctamente\n")

    except Exception as e:
        print(f"✗ [FAIL] Error: {e}\n")
        raise


@pytest.mark.order(5)
def test_05_listar_movimientos():
    """GET /volantes/{id}/movimientos — Listar movimientos de un volante."""

    try:
        response = requests.get(
            f"{API_URL}/asistente/volantes/{VOLANTE_ID}/movimientos",
            headers=get_headers(),
            timeout=TIMEOUT
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        movimientos = data["data"]

        print(f"  ✓ Movimientos encontrados: {len(movimientos)}")
        for mov in movimientos:
            print(f"    - {mov['codigo_detalle']}: ${mov['valor']} ({mov['fecha']})")

        print("✓ [OK] Movimientos listados correctamente\n")

    except Exception as e:
        print(f"✗ [FAIL] Error: {e}\n")
        raise


# =============================================
# TESTS: PAGOS
# =============================================

@pytest.mark.order(6)
def test_06_registrar_pago():
    """POST /pagos — Registrar pago parcial (50%) para un volante."""
    global TRANSACCION_ID

    try:
        # Obtener monto total del volante
        resp_volante = requests.get(
            f"{API_URL}/asistente/volantes/{VOLANTE_ID}",
            headers=get_headers(),
            timeout=TIMEOUT
        )
        monto_total = resp_volante.json()["data"]["monto_total"]
        monto_pago = monto_total * 0.5  # Pagar 50%

        payload = {
            "id_volante": VOLANTE_ID,
            "medio_pago": "Transferencia Bancaria",
            "valor": monto_pago,
            "referencia": f"REF-{int(time.time())}"
        }

        response = requests.post(
            f"{API_URL}/asistente/pagos",
            json=payload,
            headers=get_headers(),
            timeout=TIMEOUT
        )

        assert response.status_code == 200, f"Error: {response.text}"
        data = response.json()
        assert data["success"] is True

        TRANSACCION_ID = data["data"]["id_transaccion"]
        print(f"  ✓ Pago registrado: ${payload['valor']}")
        print(f"  ✓ Transacción ID: {TRANSACCION_ID}")
        print(f"  ✓ Referencia: {payload['referencia']}")
        print(f"  ✓ Volante estado cambió a: PARCIAL (50% pagado)")
        print("✓ [OK] Pago registrado correctamente\n")

    except Exception as e:
        print(f"✗ [FAIL] Error: {e}\n")
        raise


@pytest.mark.order(7)
def test_07_verificar_estado_volante_parcial():
    """GET /volantes/{id} — Verificar que volante cambió a PARCIAL."""

    try:
        response = requests.get(
            f"{API_URL}/asistente/volantes/{VOLANTE_ID}",
            headers=get_headers(),
            timeout=TIMEOUT
        )

        assert response.status_code == 200
        data = response.json()
        estado = data["data"]["estado"]

        assert estado == "PARCIAL", f"Estado esperado PARCIAL, obtuvimos: {estado}"
        print(f"  ✓ Volante estado: {estado}")
        print("✓ [OK] Estado actualizado correctamente (PARCIAL)\n")

    except Exception as e:
        print(f"✗ [FAIL] Error: {e}\n")
        raise


@pytest.mark.order(8)
def test_08_registrar_segundo_pago():
    """POST /pagos — Registrar segundo pago para completar volante (50% restante)."""

    try:
        # Obtener monto total actual
        resp_volante = requests.get(
            f"{API_URL}/asistente/volantes/{VOLANTE_ID}",
            headers=get_headers(),
            timeout=TIMEOUT
        )
        monto_total = resp_volante.json()["data"]["monto_total"]
        # Pagar el 50% restante (no el monto total completo)
        monto_restante = monto_total * 0.5

        payload = {
            "id_volante": VOLANTE_ID,
            "medio_pago": "Efectivo",
            "valor": monto_restante,
            "referencia": f"EF-{int(time.time())}"
        }

        response = requests.post(
            f"{API_URL}/asistente/pagos",
            json=payload,
            headers=get_headers(),
            timeout=TIMEOUT
        )

        assert response.status_code == 200, f"Error: {response.text}"
        data = response.json()
        assert data["success"] is True

        print(f"  ✓ Pago completo registrado: ${payload['valor']}")
        print(f"  ✓ Volante estado cambió a: PAGADO (100% cancelado)")
        print("✓ [OK] Segundo pago registrado correctamente\n")

    except Exception as e:
        print(f"✗ [FAIL] Error: {e}\n")
        raise


@pytest.mark.order(9)
def test_09_verificar_estado_volante_pagado():
    """GET /volantes/{id} — Verificar que volante cambió a PAGADO."""

    try:
        response = requests.get(
            f"{API_URL}/asistente/volantes/{VOLANTE_ID}",
            headers=get_headers(),
            timeout=TIMEOUT
        )

        assert response.status_code == 200
        data = response.json()
        estado = data["data"]["estado"]

        assert estado == "PAGADO", f"Estado esperado PAGADO, obtuvimos: {estado}"
        print(f"  ✓ Volante estado: {estado}")
        print("✓ [OK] Volante completamente pagado\n")

    except Exception as e:
        print(f"✗ [FAIL] Error: {e}\n")
        raise


# =============================================
# TESTS: ELIMINACIÓN DE MOVIMIENTOS
# =============================================

@pytest.mark.order(10)
def test_10_eliminar_movimiento():
    """DELETE /movimientos/{id} — Eliminar un movimiento (cobro adicional PLAB)."""

    try:
        # Obtener movimientos del volante
        resp_mov = requests.get(
            f"{API_URL}/asistente/volantes/{VOLANTE_ID}/movimientos",
            headers=get_headers(),
            timeout=TIMEOUT
        )

        movimientos = resp_mov.json()["data"]
        if not movimientos:
            print("  ⚠ No hay movimientos para eliminar")
            print("✓ [OK] Test saltado (sin movimientos)\n")
            return

        # Buscar el movimiento de cobro adicional (PLAB) para eliminar
        # Evitamos eliminar el cobro principal (PMAT/PCRE) o los pagos (MPAG)
        id_mov_eliminar = None
        for mov in movimientos:
            if mov["codigo_detalle"] in ["PLAB", "PCAR", "PEXA"]:
                id_mov_eliminar = mov["id_mov"]
                break

        if not id_mov_eliminar:
            # Si no hay cobro adicional, usar el último movimiento
            id_mov_eliminar = movimientos[-1]["id_mov"]

        response = requests.delete(
            f"{API_URL}/asistente/movimientos/{id_mov_eliminar}",
            headers=get_headers(),
            timeout=TIMEOUT
        )

        assert response.status_code == 200, f"Error: {response.text}"
        data = response.json()
        assert data["success"] is True

        print(f"  ✓ Movimiento {id_mov_eliminar} eliminado")
        print("✓ [OK] Movimiento eliminado correctamente\n")

    except Exception as e:
        print(f"✗ [FAIL] Error: {e}\n")
        raise


# =============================================
# TESTS: AUTORIZACIÓN
# =============================================

@pytest.mark.order(11)
def test_11_autorizar_acceso_asistente():
    """Verificar que solo ASISTENTE y ADMINISTRADOR pueden acceder."""

    try:
        # Sin token debe fallar
        response = requests.get(f"{API_URL}/asistente/volantes", timeout=TIMEOUT)
        assert response.status_code in [401, 403], "Debe fallar sin token"

        # Con token de ASISTENTE debe funcionar
        response = requests.get(f"{API_URL}/asistente/volantes", headers=get_headers(), timeout=TIMEOUT)
        assert response.status_code == 200, "Debe funcionar con token ASISTENTE"

        print("  ✓ Autorización correcta: sin token → 401/403")
        print("  ✓ Autorización correcta: con token ASISTENTE → 200")
        print("✓ [OK] Autorización validada correctamente\n")

    except Exception as e:
        print(f"✗ [FAIL] Error: {e}\n")
        raise


# =============================================
# EJECUTAR TESTS
# =============================================
if __name__ == "__main__":
    print("\n" + "="*60)
    print("ETAPA 6: TESTS ASISTENTE - LÓGICA DE COBROS")
    print("="*60)

    exit_code = pytest.main([__file__, "-v", "--tb=short", "-p", "no:warnings"])

    if exit_code == 0:
        print("\n" + "="*60)
        print("[OK] TODOS LOS TESTS PASARON ✓")
        print("="*60 + "\n")
    else:
        print("\n" + "="*60)
        print("[FAIL] ALGUNOS TESTS FALLARON ✗")
        print("="*60 + "\n")

    sys.exit(exit_code)
