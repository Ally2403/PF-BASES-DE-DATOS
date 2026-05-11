#!/usr/bin/env python3
"""
Aplicar corrección del trigger directamente sin pool
"""
import oracledb
import sys
import os

# Leer credenciales del entorno o usar defaults
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', '1521'))
DB_SERVICE = os.getenv('DB_SERVICE', 'xe')
DB_USER = os.getenv('DB_USER', 'app_user').lower()
DB_PASSWORD = os.getenv('DB_PASSWORD', 'app_user')

print(f"📡 Conectando a {DB_HOST}:{DB_PORT}/{DB_SERVICE} como {DB_USER}")

try:
    # Conexión simple
    conn = oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        service_name=DB_SERVICE
    )
    cursor = conn.cursor()
    print("✅ Conexión exitosa\n")
    
    # SQL para crear trigger COMPOUND
    sql = """
    CREATE OR REPLACE TRIGGER TR_RECALCULAR_MONTO_VOLANTE
    FOR INSERT ON MOVIMIENTO
    COMPOUND TRIGGER
        TYPE t_volante_ids IS TABLE OF MOVIMIENTO.ID_VOLANTE%TYPE;
        v_volante_ids t_volante_ids := t_volante_ids();
        
        AFTER EACH ROW IS
        BEGIN
            IF :NEW.ID_VOLANTE IS NOT NULL THEN
                v_volante_ids.EXTEND;
                v_volante_ids(v_volante_ids.LAST) := :NEW.ID_VOLANTE;
            END IF;
        END AFTER EACH ROW;
        
        AFTER STATEMENT IS
        BEGIN
            FOR i IN 1 .. v_volante_ids.COUNT LOOP
                DECLARE
                    v_id_volante    MOVIMIENTO.ID_VOLANTE%TYPE := v_volante_ids(i);
                    v_nuevo_monto   NUMBER(15, 2);
                BEGIN
                    SELECT NVL(SUM(m.VALOR), 0) INTO v_nuevo_monto
                    FROM   MOVIMIENTO m
                    JOIN   CODIGO_DETALLE cd ON cd.CODIGO_DETALLE = m.CODIGO_DETALLE
                    WHERE  m.ID_VOLANTE = v_id_volante
                      AND  cd.GRUPO = 'COBRO';
                    
                    UPDATE VOLANTE_MATRICULA
                    SET    MONTO_TOTAL = v_nuevo_monto
                    WHERE  ID_VOLANTE = v_id_volante;
                END;
            END LOOP;
        END AFTER STATEMENT;
    END TR_RECALCULAR_MONTO_VOLANTE;
    """
    
    print("🔧 Aplicando corrección del trigger...")
    cursor.execute(sql)
    conn.commit()
    print("✅ Trigger actualizado exitosamente\n")
    
    # Verificar que existe
    cursor.execute("""
        SELECT trigger_name, trigger_type, triggering_event
        FROM user_triggers
        WHERE trigger_name = 'TR_RECALCULAR_MONTO_VOLANTE'
    """)
    result = cursor.fetchone()
    if result:
        print(f"✅ Verificación exitosa:")
        print(f"   Nombre: {result[0]}")
        print(f"   Tipo: {result[1]}")
        print(f"   Evento: {result[2]}")
    
    conn.close()
    print("\n✅ Corrección completada")
    sys.exit(0)
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
