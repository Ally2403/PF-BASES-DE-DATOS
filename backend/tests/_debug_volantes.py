import requests

API = "http://localhost:8000/api"

# Login
token = requests.post(f"{API}/auth/login", json={"username": "ltorres", "password": "password123"}).json()["data"]["access_token"]
h = {"Authorization": f"Bearer {token}"}

# List volantes
r = requests.get(f"{API}/asistente/volantes", headers=h)
print(f"Status: {r.status_code}")
body = r.json()
print(f"Response keys: {list(body.keys())}")

if "data" in body:
    for v in body["data"]:
        vid = v["id_volante"]
        print(f"  ID={vid}, est={v['id_estudiante']}, per={v['id_periodo']}, estado={v['estado']}, monto={v['monto_total']}")
        
        r2 = requests.get(f"{API}/asistente/volantes/{vid}/movimientos", headers=h)
        if r2.status_code == 200:
            movs = r2.json()["data"]
            for m in movs:
                print(f"    MOV id={m['id_mov']}, cod={m['codigo_detalle']}, val={m['valor']}")
            if not movs:
                print("    (sin movimientos)")
else:
    print(f"Body: {body}")

# Also try listar volantes endpoint
print("\n--- GET estudiantes via admin ---")
token_admin = requests.post(f"{API}/auth/login", json={"username": "cmendoza", "password": "password123"}).json()["data"]["access_token"]
ha = {"Authorization": f"Bearer {token_admin}"}
r3 = requests.get(f"{API}/estudiantes", headers=ha)
estudiantes = r3.json()["data"]
print(f"Estudiantes: {len(estudiantes)}")
if estudiantes:
    print(f"  Primer estudiante: ID={estudiantes[0]['id_estudiante']}")
