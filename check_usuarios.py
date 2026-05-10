#!/usr/bin/env python
"""Verifica usuarios disponibles en BD"""
import sys
sys.path.insert(0, 'backend')

from app.services.database import OracleConnection

try:
    with OracleConnection() as conn:
        print("\n" + "="*60)
        print("USUARIOS EN BD")
        print("="*60)
        
        usuarios = conn.execute_query(
            'SELECT ID_USUARIO, NOMBRE_USUARIO, ID_PERFIL FROM USUARIO FETCH FIRST 10 ROWS ONLY'
        )
        if usuarios:
            for u in usuarios:
                print(f"\n  Usuario: {u['NOMBRE_USUARIO']}")
                print(f"    ID: {u['ID_USUARIO']}")
                print(f"    Perfil ID: {u['ID_PERFIL']}")
        else:
            print("\n  ⚠ No se encontraron usuarios")
        
        print("\n" + "="*60)
        print("PERFILES DISPONIBLES")
        print("="*60)
        
        perfiles = conn.execute_query(
            'SELECT ID_PERFIL, NOMBRE_PERFIL FROM PERFIL FETCH FIRST 10 ROWS ONLY'
        )
        if perfiles:
            for p in perfiles:
                print(f"  - {p['NOMBRE_PERFIL']} (ID: {p['ID_PERFIL']})")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
