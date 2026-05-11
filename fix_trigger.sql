SET ECHO ON
SET FEEDBACK ON

PROMPT ==========================================
PROMPT Aplicando corrección del trigger ORA-04091
PROMPT ==========================================

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
/

PROMPT ==========================================
PROMPT Verificando que el trigger fue creado
PROMPT ==========================================
SELECT TRIGGER_NAME, TRIGGER_TYPE, TRIGGERING_EVENT
FROM USER_TRIGGERS
WHERE TRIGGER_NAME = 'TR_RECALCULAR_MONTO_VOLANTE';

PROMPT
PROMPT ==========================================
PROMPT Corrección completada
PROMPT ==========================================
EXIT;
