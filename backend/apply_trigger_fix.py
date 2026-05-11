#!/usr/bin/env python3
"""
Script para aplicar la corrección del trigger TR_RECALCULAR_MONTO_VOLANTE
Convierte de FOR EACH ROW a COMPOUND TRIGGER para evitar ORA-04091
"""

import oracledb
import sys

# Configuración de conexión Oracle
DB_CONFIG = {
    'host': 'localhost',
    'port': 1521,
    'service_name': 'xe',
    'user': 'system',
    'password': 'system'
}

# Script SQL para la corrección
TRIGGER_CORRECCION = """
CREATE OR REPLACE TRIGGER TR_RECALCULAR_MONTO_VOLANTE
FOR INSERT ON MOVIMIENTO
COMPOUND TRIGGER

    -- Tabla local para acumular IDs de volantes a procesar
    TYPE t_volante_ids IS TABLE OF MOVIMIENTO.ID_VOLANTE%TYPE;
    v_volante_ids t_volante_ids := t_volante_ids();

    -- Sección: Cada fila insertada
    AFTER EACH ROW IS
    BEGIN
        IF :NEW.ID_VOLANTE IS NOT NULL THEN
            -- Solo acumular volantes nuevos (evitar duplicados)
            IF v_volante_ids.COUNT = 0 OR
               :NEW.ID_VOLANTE NOT IN (SELECT * FROM TABLE(v_volante_ids)) THEN
                v_volante_ids.EXTEND;
                v_volante_ids(v_volante_ids.LAST) := :NEW.ID_VOLANTE;
            END IF;
        END IF;
    END AFTER EACH ROW;

    -- Sección: Después de todas las inserciones
    AFTER STATEMENT IS
    BEGIN
        -- Ahora que la mutación terminó, podemos hacer SELECT
        FOR i IN 1 .. v_volante_ids.COUNT LOOP
            DECLARE
                v_id_volante    MOVIMIENTO.ID_VOLANTE%TYPE := v_volante_ids(i);
                v_nuevo_monto   NUMBER(15, 2);
            BEGIN
                -- Calcular suma de COBROs del volante
                SELECT NVL(SUM(m.VALOR), 0) INTO v_nuevo_monto
                FROM   MOVIMIENTO m
                JOIN   CODIGO_DETALLE cd ON cd.CODIGO_DETALLE = m.CODIGO_DETALLE
                WHERE  m.ID_VOLANTE = v_id_volante
                  AND  cd.GRUPO = 'COBRO';

                -- Actualizar MONTO_TOTAL del volante
                UPDATE VOLANTE_MATRICULA
                SET    MONTO_TOTAL = v_nuevo_monto
                WHERE  ID_VOLANTE = v_id_volante;
            END;
        END LOOP;
    END AFTER STATEMENT;

END TR_RECALCULAR_MONTO_VOLANTE;
"""

def apply_trigger_fix():
    """Conecta a Oracle y aplica la corrección del trigger"""
    try:
        # Conectar directamente a Oracle
        conn = oracledb.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            service_name=DB_CONFIG['service_name'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        
        cursor = conn.cursor()
        
        print("✓ Conectado a Oracle Database")
        print("✓ Aplicando corrección de trigger TR_RECALCULAR_MONTO_VOLANTE...")
        
        # Ejecutar el script de corrección
        cursor.execute(TRIGGER_CORRECCION)
        
        print("✓ Trigger convertido a COMPOUND TRIGGER exitosamente")
        print("✓ Correccion aplicada: ORA-04091 debe estar resuelto")
        
        # Verificar que el trigger exista
        cursor.execute("""
            SELECT TRIGGER_NAME, TRIGGER_TYPE, TRIGGERING_EVENT
            FROM USER_TRIGGERS
            WHERE TRIGGER_NAME = 'TR_RECALCULAR_MONTO_VOLANTE'
        """)
        
        result = cursor.fetchone()
        if result:
            print(f"✓ Verificación: Trigger existe")
            print(f"  - Nombre: {result[0]}")
            print(f"  - Tipo: {result[1]}")
            print(f"  - Evento: {result[2]}")
        
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Error al aplicar corrección: {e}")
        return False

if __name__ == "__main__":
    success = apply_trigger_fix()
    sys.exit(0 if success else 1)
