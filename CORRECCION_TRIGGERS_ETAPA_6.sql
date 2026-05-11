-- ============================================================
-- CORRECION DE TRIGGERS - Etapa 6
-- ============================================================
-- Problema: TR_RECALCULAR_MONTO_VOLANTE causa ORA-04091
-- Solución: Convertir a COMPOUND TRIGGER
-- ============================================================

-- DROP del trigger viejo (si existe)
BEGIN
    EXECUTE IMMEDIATE 'DROP TRIGGER TR_RECALCULAR_MONTO_VOLANTE';
EXCEPTION
    WHEN OTHERS THEN NULL;
END;
/

-- NUEVO TRIGGER 7.6: TR_RECALCULAR_MONTO_VOLANTE (COMPOUND)
-- Recalcula MONTO_TOTAL del volante cada vez que se inserta
-- un movimiento de tipo COBRO asociado a ese volante.
-- Cubre cobros adicionales como PCAR, PLAB, PEXA que se
-- agregan después de generar el volante inicial.
-- Usa COMPOUND TRIGGER para evitar ORA-04091 (tabla mutando).
-- ----------------------------------------------------------
CREATE OR REPLACE TRIGGER TR_RECALCULAR_MONTO_VOLANTE
FOR INSERT ON MOVIMIENTO
COMPOUND TRIGGER

    TYPE t_volantes IS TABLE OF NUMBER INDEX BY PLS_INTEGER;
    v_volantes  t_volantes;
    v_idx       PLS_INTEGER := 0;

    AFTER EACH ROW IS
        v_grupo         CODIGO_DETALLE.GRUPO%TYPE;
        v_duplicado     BOOLEAN := FALSE;
    BEGIN
        -- Solo procesar si es un movimiento de COBRO
        SELECT GRUPO INTO v_grupo
        FROM   CODIGO_DETALLE
        WHERE  CODIGO_DETALLE = :NEW.CODIGO_DETALLE;

        IF v_grupo = 'COBRO' AND :NEW.ID_VOLANTE IS NOT NULL THEN
            -- Verificar que el volante no esté ya en la coleccion
            FOR i IN 1 .. v_idx LOOP
                IF v_volantes(i) = :NEW.ID_VOLANTE THEN
                    v_duplicado := TRUE;
                    EXIT;
                END IF;
            END LOOP;
            
            IF NOT v_duplicado THEN
                v_idx := v_idx + 1;
                v_volantes(v_idx) := :NEW.ID_VOLANTE;
            END IF;
        END IF;
    END AFTER EACH ROW;

    AFTER STATEMENT IS
        v_nuevo_monto NUMBER(15, 2);
    BEGIN
        -- Procesar todos los volantes acumulados
        FOR i IN 1 .. v_volantes.COUNT LOOP
            -- Sumar todos los movimientos de COBRO del volante
            SELECT NVL(SUM(m.VALOR), 0) INTO v_nuevo_monto
            FROM   MOVIMIENTO m
            JOIN   CODIGO_DETALLE cd ON cd.CODIGO_DETALLE = m.CODIGO_DETALLE
            WHERE  m.ID_VOLANTE = v_volantes(i)
              AND  cd.GRUPO     = 'COBRO';

            UPDATE VOLANTE_MATRICULA
            SET    MONTO_TOTAL = v_nuevo_monto
            WHERE  ID_VOLANTE  = v_volantes(i);
        END LOOP;
    END AFTER STATEMENT;

END TR_RECALCULAR_MONTO_VOLANTE;
/

-- ============================================================
-- VERIFICACION: Confirmar que ambos triggers existen
-- ============================================================

SELECT TRIGGER_NAME, TRIGGER_TYPE, TRIGGERING_EVENT
FROM   USER_TRIGGERS
WHERE  TRIGGER_NAME IN ('TR_ACTUALIZAR_ESTADO_VOLANTE', 'TR_RECALCULAR_MONTO_VOLANTE')
ORDER BY TRIGGER_NAME;

PROMPT
PROMPT >>> Triggers corregidos exitosamente
PROMPT >>> TR_ACTUALIZAR_ESTADO_VOLANTE: COMPOUND TRIGGER (ya existía)
PROMPT >>> TR_RECALCULAR_MONTO_VOLANTE: COMPOUND TRIGGER (corregido)
PROMPT

-- ============================================================
-- TEST: Verificar que los triggers funcionan
-- ============================================================

-- Test 1: Crear un volante
DECLARE
    v_id_volante NUMBER;
BEGIN
    SELECT SEQ_VOLANTE.NEXTVAL INTO v_id_volante FROM DUAL;
    INSERT INTO VOLANTE_MATRICULA
    (ID_VOLANTE, ID_ESTUDIANTE, ID_PERIODO, ID_PROGRAMA, MODALIDAD, 
     SEMESTRE_QUE_COBRA, TIPO_GENERACION, ESTADO, FECHA_GENERACION)
    VALUES (v_id_volante, 1, 1, 1, 'GLOBAL', 1, 'TEST', 'PENDIENTE', SYSDATE);
    COMMIT;
    DBMS_OUTPUT.PUT_LINE('✓ Volante test creado: ' || v_id_volante);
END;
/

-- Test 2: Agregar un cobro adicional
DECLARE
    v_id_mov NUMBER;
    v_id_volante NUMBER := 1;
    v_id_cuenta  NUMBER;
BEGIN
    -- Obtener cuenta del estudiante
    SELECT ID_CUENTA INTO v_id_cuenta
    FROM   CUENTA_CORRIENTE
    WHERE  ID_ESTUDIANTE = 1 AND ID_PERIODO = 1
    AND    ROWNUM = 1;

    -- Insertar movimiento de cobro adicional
    SELECT SEQ_MOVIMIENTO.NEXTVAL INTO v_id_mov FROM DUAL;
    INSERT INTO MOVIMIENTO
    (ID_MOV, FECHA, VALOR, CODIGO_DETALLE, ID_VOLANTE, ID_PERIODO, ID_CUENTA)
    VALUES (v_id_mov, SYSDATE, 50000, 'PLAB', v_id_volante, 1, v_id_cuenta);
    COMMIT;
    
    DBMS_OUTPUT.PUT_LINE('✓ Cobro adicional insertado (PLAB): ' || v_id_mov);
EXCEPTION WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('✗ Error en test: ' || SQLERRM);
END;
/

-- Verificar que MONTO_TOTAL se actualizó
SELECT ID_VOLANTE, MONTO_TOTAL, ESTADO 
FROM VOLANTE_MATRICULA 
WHERE ID_VOLANTE = 1;

PROMPT
PROMPT >>> Si MONTO_TOTAL != 0, el trigger funcionó correctamente
PROMPT

-- ============================================================
-- LIMPIEZA DE DATOS TEST (opcional)
-- ============================================================

-- DELETE FROM MOVIMIENTO WHERE ID_VOLANTE = 1;
-- DELETE FROM VOLANTE_MATRICULA WHERE ID_VOLANTE = 1;
-- COMMIT;

PROMPT
PROMPT >>> Correcciones completadas. Ejecuta tests nuevamente.
PROMPT
