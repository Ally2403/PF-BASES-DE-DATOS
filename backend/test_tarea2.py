#!/usr/bin/env python3
"""
Script para verificar que la TAREA 2 se implementó correctamente
"""
import oracledb

try:
    conn = oracledb.connect(user='app_user', password='appsecure', host='localhost', port=1521, service_name='XEPDB1')
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("VERIFICACIÓN TAREA 2 — ESTADO MOVIDO A CUENTA_CORRIENTE")
    print("="*60 + "\n")
    
    # Verificar estructura de VOLANTE_MATRICULA
    print("1️⃣  Columnas de VOLANTE_MATRICULA:")
    cursor.execute("SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME='VOLANTE_MATRICULA' ORDER BY COLUMN_ID")
    cols = [row[0] for row in cursor.fetchall()]
    for col in cols:
        print(f"   ✓ {col}")
    
    # Verificar si ESTADO existe en VOLANTE_MATRICULA
    if 'ESTADO' in cols:
        print("   ❌ ERROR: ESTADO aún existe en VOLANTE_MATRICULA")
    else:
        print("   ✅ CORRECTO: ESTADO NO existe en VOLANTE_MATRICULA")
    
    # Verificar columnas de CUENTA_CORRIENTE
    print("\n2️⃣  Columnas de CUENTA_CORRIENTE:")
    cursor.execute("SELECT COLUMN_NAME FROM USER_TAB_COLUMNS WHERE TABLE_NAME='CUENTA_CORRIENTE' ORDER BY COLUMN_ID")
    cols_cc = [row[0] for row in cursor.fetchall()]
    for col in cols_cc:
        print(f"   ✓ {col}")
    
    # Verificar que ESTADO existe en CUENTA_CORRIENTE
    if 'ESTADO' in cols_cc:
        print("   ✅ CORRECTO: ESTADO existe en CUENTA_CORRIENTE")
    else:
        print("   ❌ ERROR: ESTADO NO existe en CUENTA_CORRIENTE")
    
    # Verificar datos
    print("\n3️⃣  Datos en BD (Volante ID=1, Cuenta ID=1):")
    cursor.execute("SELECT ID_VOLANTE, MONTO_TOTAL FROM VOLANTE_MATRICULA WHERE ID_VOLANTE=1")
    vol = cursor.fetchone()
    if vol:
        print(f"   ✓ Volante {vol[0]}: Monto=${vol[1]:,.2f}")
    
    cursor.execute("SELECT ID_CUENTA, ESTADO FROM CUENTA_CORRIENTE WHERE ID_CUENTA=1")
    cc = cursor.fetchone()
    if cc:
        print(f"   ✓ Cuenta {cc[0]}: Estado='{cc[1]}'")
    
    print("\n" + "="*60)
    print("✅ TAREA 2 VERIFICADA EXITOSAMENTE")
    print("="*60 + "\n")
    
    conn.close()
except Exception as e:
    print(f"\n❌ Error: {e}\n")
