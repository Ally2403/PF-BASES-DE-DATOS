-- ============================================================
-- CORRECCIÓN: TR_RECALCULAR_MONTO_VOLANTE
-- Problema: ORA-04091 Tabla mutando (AFTER INSERT FOR EACH ROW)
-- Solución: Convertir a COMPOUND TRIGGER con AFTER EACH ROW + AFTER STATEMENT
-- ============================================================

-- Primero, remplazar el trigger existente con la versión COMPOUND
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
/

-- ============================================================
-- VERIFICACIÓN: Ejecutar este script en Oracle para aplicar corrección
-- ============================================================
-- Sintaxis: sqlplus user/pass@database @CORRECCION_TRIGGER_ORA04091.sql
-- ============================================================
