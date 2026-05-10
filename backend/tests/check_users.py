import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.database import OracleConnection

with OracleConnection() as conn:
    usuarios = conn.execute_query(
        'SELECT ID_USUARIO, NOMBRE_USUARIO, ID_PERFIL FROM USUARIO FETCH FIRST 10 ROWS ONLY'
    )
    print('Usuarios disponibles:')
    for u in usuarios:
        print(f'  - {u["NOMBRE_USUARIO"]} (ID: {u["ID_USUARIO"]}, Perfil: {u["ID_PERFIL"]})')
