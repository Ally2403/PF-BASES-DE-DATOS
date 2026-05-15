-- ============================================================
-- IST7111 - Bases de Datos 2026-10 | NRC 2076
-- SCRIPT COMPLETO - Entregables #3, #4 y #5
-- Cuenta Corriente del Estudiante
-- ============================================================
-- Orden de ejecucion:
--   1. DROP tablas y secuencias
--   2. CREATE secuencias
--   3. CREATE tablas
--   4. CREATE indices
--   5. INSERT datos semilla
--   6. CREATE triggers
--   7. CREATE vistas
-- ============================================================


-- ============================================================
-- SECCION 1: DROP DE TABLAS (dependientes primero)
-- ============================================================

PROMPT >>> Eliminando tablas existentes...

BEGIN EXECUTE IMMEDIATE 'DROP TABLE VOLANTE_MATRICULA_ASIGNATURA CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE TRANSACCION_PAGO            CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE MOVIMIENTO                  CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE CUENTA_CORRIENTE            CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE VOLANTE_MATRICULA           CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE PLAN_ESTUDIO_ASIGNATURA     CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE PLAN_ESTUDIO                CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE REGLA_COBRO                 CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE PERFIL_PERMISO              CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE ESTUDIANTE                  CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE USUARIO                     CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE PERSONA                     CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE PERMISO                     CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE MENU                        CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE PERFIL                      CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE ASIGNATURA                  CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE CODIGO_DETALLE              CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE PROGRAMA_ACADEMICO          CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP TABLE PERIODO_ACADEMICO           CASCADE CONSTRAINTS'; EXCEPTION WHEN OTHERS THEN NULL; END;
/

PROMPT >>> Tablas eliminadas.


-- ============================================================
-- SECCION 2: DROP DE SECUENCIAS
-- ============================================================

PROMPT >>> Eliminando secuencias existentes...

BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE SEQ_PERFIL';        EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE SEQ_MENU';          EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE SEQ_PERMISO';       EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE SEQ_USUARIO';       EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE SEQ_PROGRAMA';      EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE SEQ_PERIODO';       EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE SEQ_ASIGNATURA';    EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE SEQ_ESTUDIANTE';    EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE SEQ_CUENTA';        EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE SEQ_VOLANTE';       EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE SEQ_MOVIMIENTO';    EXCEPTION WHEN OTHERS THEN NULL; END;
/
BEGIN EXECUTE IMMEDIATE 'DROP SEQUENCE SEQ_TRANSACCION';   EXCEPTION WHEN OTHERS THEN NULL; END;
/

PROMPT >>> Secuencias eliminadas.


-- ============================================================
-- SECCION 3: CREACION DE SECUENCIAS
-- ============================================================

PROMPT >>> Creando secuencias...

CREATE SEQUENCE SEQ_PERFIL       START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_MENU         START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_PERMISO      START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_USUARIO      START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_PROGRAMA     START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_PERIODO      START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_ASIGNATURA   START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_ESTUDIANTE   START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_CUENTA       START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_VOLANTE      START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_MOVIMIENTO   START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE SEQ_TRANSACCION  START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;

PROMPT >>> Secuencias creadas. (12 secuencias)


-- ============================================================
-- SECCION 4: CREACION DE TABLAS
-- Orden estricto: padre antes que hijo.
-- ============================================================

PROMPT >>> Creando tablas...

-- ----------------------------------------------------------
-- 4.1 PERFIL
-- ----------------------------------------------------------
CREATE TABLE PERFIL (
    ID_PERFIL       NUMBER          DEFAULT SEQ_PERFIL.NEXTVAL,
    NOMBRE_PERFIL   VARCHAR2(50)    NOT NULL,
    CONSTRAINT PK_PERFIL    PRIMARY KEY (ID_PERFIL)
);

-- ----------------------------------------------------------
-- 4.2 MENU
-- ----------------------------------------------------------
CREATE TABLE MENU (
    ID_MENU         NUMBER          DEFAULT SEQ_MENU.NEXTVAL,
    NOMBRE_FUNCION  VARCHAR2(100)   NOT NULL,
    URL_ACCESO      VARCHAR2(200),
    CONSTRAINT PK_MENU      PRIMARY KEY (ID_MENU)
);

-- ----------------------------------------------------------
-- 4.3 PERMISO
-- ----------------------------------------------------------
CREATE TABLE PERMISO (
    ID_PERMISO          NUMBER          DEFAULT SEQ_PERMISO.NEXTVAL,
    NOMBRE_OPERACION    VARCHAR2(100)   NOT NULL,
    DESCRIPCION         VARCHAR2(300),
    ID_MENU             NUMBER,
    CONSTRAINT PK_PERMISO   PRIMARY KEY (ID_PERMISO),
    CONSTRAINT FK_PERM_MENU FOREIGN KEY (ID_MENU)
        REFERENCES MENU(ID_MENU) ON DELETE CASCADE
);

-- ----------------------------------------------------------
-- 4.4 PROGRAMA_ACADEMICO
-- CODIGO_PROGRAMA: sigla del programa (ej. SIS, ADM, MED).
-- Se usa como componente central del carnet auto-generado.
-- ----------------------------------------------------------
CREATE TABLE PROGRAMA_ACADEMICO (
    ID_PROGRAMA      NUMBER          DEFAULT SEQ_PROGRAMA.NEXTVAL,
    NOMBRE_PROGRAMA  VARCHAR2(200)   NOT NULL,
    CODIGO_PROGRAMA  VARCHAR2(10)    NOT NULL,
    CONSTRAINT PK_PROGRAMA       PRIMARY KEY (ID_PROGRAMA),
    CONSTRAINT UQ_PROG_CODIGO    UNIQUE (CODIGO_PROGRAMA)
);

-- ----------------------------------------------------------
-- 4.5 PERIODO_ACADEMICO
-- ----------------------------------------------------------
CREATE TABLE PERIODO_ACADEMICO (
    ID_PERIODO      NUMBER          DEFAULT SEQ_PERIODO.NEXTVAL,
    NOMBRE_PERIODO  VARCHAR2(20)    NOT NULL,
    FECHA_INICIO    DATE            NOT NULL,
    FECHA_FIN       DATE            NOT NULL,
    CONSTRAINT PK_PERIODO       PRIMARY KEY (ID_PERIODO),
    CONSTRAINT UQ_PER_NOMBRE    UNIQUE (NOMBRE_PERIODO),
    CONSTRAINT CK_PER_FECHAS    CHECK (FECHA_FIN > FECHA_INICIO)
);

-- ----------------------------------------------------------
-- 4.6 ASIGNATURA
-- ----------------------------------------------------------
CREATE TABLE ASIGNATURA (
    ID_ASIGNATURA   NUMBER          DEFAULT SEQ_ASIGNATURA.NEXTVAL,
    NOMBRE          VARCHAR2(200)   NOT NULL,
    CANT_CREDITOS   NUMBER(2)       NOT NULL,
    CONSTRAINT PK_ASIGNATURA    PRIMARY KEY (ID_ASIGNATURA),
    CONSTRAINT CK_ASIG_CRED     CHECK (CANT_CREDITOS BETWEEN 1 AND 10)
);

-- ----------------------------------------------------------
-- 4.7 CODIGO_DETALLE
-- GRUPO: COBRO = cargo al estudiante, PAGO = abono.
-- ----------------------------------------------------------
CREATE TABLE CODIGO_DETALLE (
    CODIGO_DETALLE  VARCHAR2(10),
    GRUPO           VARCHAR2(10)    NOT NULL,
    DESCRIPCION     VARCHAR2(200)   NOT NULL,
    VALOR_DEFECTO   NUMBER(12,2)    DEFAULT NULL,
    CONSTRAINT PK_CODIGO_DET    PRIMARY KEY (CODIGO_DETALLE),
    CONSTRAINT CK_COD_GRU       CHECK (GRUPO IN ('COBRO', 'PAGO'))
);

-- ----------------------------------------------------------
-- 4.8 PERSONA
-- ----------------------------------------------------------
CREATE TABLE PERSONA (
    CEDULA      NUMBER(12)      NOT NULL,
    NOMBRE      VARCHAR2(100)   NOT NULL,
    APELLIDO    VARCHAR2(100)   NOT NULL,
    CORREO      VARCHAR2(150)   NOT NULL,
    TELEFONO    VARCHAR2(20),
    CONSTRAINT PK_PERSONA       PRIMARY KEY (CEDULA),
    CONSTRAINT UQ_PER_CORREO    UNIQUE (CORREO)
);

-- ----------------------------------------------------------
-- 4.9 PERFIL_PERMISO
-- ----------------------------------------------------------
CREATE TABLE PERFIL_PERMISO (
    ID_PERFIL   NUMBER  NOT NULL,
    ID_PERMISO  NUMBER  NOT NULL,
    CONSTRAINT PK_PERFIL_PERMISO    PRIMARY KEY (ID_PERFIL, ID_PERMISO),
    CONSTRAINT FK_PP_PERFIL         FOREIGN KEY (ID_PERFIL)
        REFERENCES PERFIL(ID_PERFIL)   ON DELETE CASCADE,
    CONSTRAINT FK_PP_PERMISO        FOREIGN KEY (ID_PERMISO)
        REFERENCES PERMISO(ID_PERMISO) ON DELETE CASCADE
);

-- ----------------------------------------------------------
-- 4.10 USUARIO
-- ----------------------------------------------------------
CREATE TABLE USUARIO (
    ID_USER     NUMBER          DEFAULT SEQ_USUARIO.NEXTVAL,
    USERNAME    VARCHAR2(50)    NOT NULL,
    CONTRASENA  VARCHAR2(256)   NOT NULL,
    ID_PERFIL   NUMBER          NOT NULL,
    CEDULA      NUMBER(12)      NOT NULL,
    CONSTRAINT PK_USUARIO       PRIMARY KEY (ID_USER),
    CONSTRAINT UQ_USR_USERNAME  UNIQUE (USERNAME),
    CONSTRAINT UQ_USR_CEDULA    UNIQUE (CEDULA),
    CONSTRAINT FK_USR_PERFIL    FOREIGN KEY (ID_PERFIL)
        REFERENCES PERFIL(ID_PERFIL) ON DELETE CASCADE,
    CONSTRAINT FK_USR_PERSONA   FOREIGN KEY (CEDULA)
        REFERENCES PERSONA(CEDULA) ON DELETE CASCADE
);

-- ----------------------------------------------------------
-- 4.11 REGLA_COBRO
-- CHECK: GLOBAL usa solo valorGlobal, CREDITOS usa solo valorCredito.
-- ----------------------------------------------------------
CREATE TABLE REGLA_COBRO (
    MODALIDAD       VARCHAR2(10)    NOT NULL,
    VALORCREDITO    NUMBER(15, 2),
    VALORGLOBAL     NUMBER(15, 2),
    ID_PROGRAMA     NUMBER          NOT NULL,
    ID_PERIODO      NUMBER          NOT NULL,
    CONSTRAINT PK_REGLA_COBRO   PRIMARY KEY (MODALIDAD, ID_PROGRAMA, ID_PERIODO),
    CONSTRAINT FK_RC_PROGRAMA   FOREIGN KEY (ID_PROGRAMA)
        REFERENCES PROGRAMA_ACADEMICO(ID_PROGRAMA) ON DELETE CASCADE,
    CONSTRAINT FK_RC_PERIODO    FOREIGN KEY (ID_PERIODO)
        REFERENCES PERIODO_ACADEMICO(ID_PERIODO) ON DELETE CASCADE,
    CONSTRAINT CK_RC_MOD        CHECK (MODALIDAD IN ('GLOBAL', 'CREDITOS')),
    CONSTRAINT CK_RC_VALS       CHECK (
        (MODALIDAD = 'GLOBAL'   AND VALORGLOBAL  IS NOT NULL AND VALORCREDITO IS NULL)
     OR (MODALIDAD = 'CREDITOS' AND VALORCREDITO IS NOT NULL AND VALORGLOBAL  IS NULL)
    ),
    CONSTRAINT CK_RC_VAL_GLOB   CHECK (VALORGLOBAL  IS NULL OR VALORGLOBAL  >= 0),
    CONSTRAINT CK_RC_VAL_CRED   CHECK (VALORCREDITO IS NULL OR VALORCREDITO >= 0)
);

-- ----------------------------------------------------------
-- 4.12 PLAN_ESTUDIO
-- ----------------------------------------------------------
CREATE TABLE PLAN_ESTUDIO (
    SEMESTRE    NUMBER(2)       NOT NULL,
    ID_PROGRAMA NUMBER          NOT NULL,
    CONSTRAINT PK_PLAN_ESTUDIO  PRIMARY KEY (SEMESTRE, ID_PROGRAMA),
    CONSTRAINT FK_PE_PROGRAMA   FOREIGN KEY (ID_PROGRAMA)
        REFERENCES PROGRAMA_ACADEMICO(ID_PROGRAMA) ON DELETE CASCADE,
    CONSTRAINT CK_PE_SEM        CHECK (SEMESTRE BETWEEN 1 AND 10)
);

-- ----------------------------------------------------------
-- 4.13 ESTUDIANTE
-- Datos propios sin FK a PERSONA.
-- ----------------------------------------------------------
CREATE TABLE ESTUDIANTE (
    ID_ESTUDIANTE   NUMBER          DEFAULT SEQ_ESTUDIANTE.NEXTVAL,
    CARNET          VARCHAR2(20),
    NOMBRE          VARCHAR2(100)   NOT NULL,
    APELLIDO        VARCHAR2(100)   NOT NULL,
    TELEFONO        VARCHAR2(20),
    CORREO          VARCHAR2(150),
    ID_PROGRAMA     NUMBER          NOT NULL,
    CONSTRAINT PK_ESTUDIANTE    PRIMARY KEY (ID_ESTUDIANTE),
    CONSTRAINT UQ_EST_CARNET    UNIQUE (CARNET),
    CONSTRAINT UQ_EST_CORREO    UNIQUE (CORREO),
    CONSTRAINT FK_EST_PROGRAMA   FOREIGN KEY (ID_PROGRAMA)
        REFERENCES PROGRAMA_ACADEMICO(ID_PROGRAMA) ON DELETE CASCADE
);

-- ----------------------------------------------------------
-- 4.14 PLAN_ESTUDIO_ASIGNATURA
-- ----------------------------------------------------------
CREATE TABLE PLAN_ESTUDIO_ASIGNATURA (
    SEMESTRE        NUMBER(2)   NOT NULL,
    ID_PROGRAMA     NUMBER      NOT NULL,
    ID_ASIGNATURA   NUMBER      NOT NULL,
    CONSTRAINT PK_PEA           PRIMARY KEY (SEMESTRE, ID_PROGRAMA, ID_ASIGNATURA),
    CONSTRAINT FK_PEA_PLAN      FOREIGN KEY (SEMESTRE, ID_PROGRAMA)
        REFERENCES PLAN_ESTUDIO(SEMESTRE, ID_PROGRAMA) ON DELETE CASCADE,
    CONSTRAINT FK_PEA_ASIG      FOREIGN KEY (ID_ASIGNATURA)
        REFERENCES ASIGNATURA(ID_ASIGNATURA) ON DELETE CASCADE
);

-- ----------------------------------------------------------
-- 4.15 CUENTA_CORRIENTE
-- PK simple. UNIQUE garantiza relacion 1:1 con estudiante.
-- Creada automaticamente por trigger al generar primer volante.
-- ----------------------------------------------------------
CREATE TABLE CUENTA_CORRIENTE (
    ID_CUENTA       NUMBER          DEFAULT SEQ_CUENTA.NEXTVAL,
    ID_ESTUDIANTE   NUMBER          NOT NULL,
    CONSTRAINT PK_CUENTA_CC         PRIMARY KEY (ID_CUENTA),
    CONSTRAINT UQ_CC_ESTUDIANTE     UNIQUE (ID_ESTUDIANTE),
    CONSTRAINT FK_CC_ESTUDIANTE     FOREIGN KEY (ID_ESTUDIANTE)
        REFERENCES ESTUDIANTE(ID_ESTUDIANTE) ON DELETE CASCADE
);

-- ----------------------------------------------------------
-- 4.16 VOLANTE_MATRICULA
-- monto_total: calculado por trigger TR_CALCULAR_MONTO_VOLANTE.
-- UNIQUE(ID_ESTUDIANTE, ID_PERIODO): un volante por estudiante
--   por periodo, independiente de la modalidad.
-- ----------------------------------------------------------
CREATE TABLE VOLANTE_MATRICULA (
    ID_VOLANTE          NUMBER          DEFAULT SEQ_VOLANTE.NEXTVAL,
    SEMESTRE_QUE_COBRA  NUMBER(2)       NOT NULL,
    FECHA_GENERACION    DATE            DEFAULT SYSDATE NOT NULL,
    TIPO_GENERACION     VARCHAR2(15)    NOT NULL,
    MONTO_TOTAL         NUMBER(15, 2)   DEFAULT 0   NOT NULL,
    ID_ESTUDIANTE       NUMBER          NOT NULL,
    ID_PERIODO          NUMBER          NOT NULL,
    MODALIDAD           VARCHAR2(10)    NOT NULL,
    ID_PROGRAMA         NUMBER          NOT NULL,
    CONSTRAINT PK_VOLANTE           PRIMARY KEY (ID_VOLANTE),
    CONSTRAINT UQ_VOL_EST_PER       UNIQUE (ID_ESTUDIANTE, ID_PERIODO),
    CONSTRAINT FK_VOL_ESTUDIANTE    FOREIGN KEY (ID_ESTUDIANTE)
        REFERENCES ESTUDIANTE(ID_ESTUDIANTE) ON DELETE CASCADE,
    CONSTRAINT FK_VOL_PERIODO       FOREIGN KEY (ID_PERIODO)
        REFERENCES PERIODO_ACADEMICO(ID_PERIODO) ON DELETE CASCADE,
    CONSTRAINT FK_VOL_PLAN          FOREIGN KEY (SEMESTRE_QUE_COBRA, ID_PROGRAMA)
        REFERENCES PLAN_ESTUDIO(SEMESTRE, ID_PROGRAMA) ON DELETE CASCADE,
    CONSTRAINT FK_VOL_REGLA         FOREIGN KEY (MODALIDAD, ID_PROGRAMA, ID_PERIODO)
        REFERENCES REGLA_COBRO(MODALIDAD, ID_PROGRAMA, ID_PERIODO) ON DELETE CASCADE,
    CONSTRAINT CK_VOL_TIPO          CHECK (TIPO_GENERACION IN ('INDIVIDUAL', 'MASIVA')),
    CONSTRAINT CK_VOL_MOD           CHECK (MODALIDAD IN ('GLOBAL', 'CREDITOS')),
    CONSTRAINT CK_VOL_SEM           CHECK (SEMESTRE_QUE_COBRA BETWEEN 1 AND 10)
);

-- ----------------------------------------------------------
-- 4.17 MOVIMIENTO
-- id_cuenta y id_periodo NOT NULL.
-- id_volante nullable: no todo movimiento viene de un volante.
-- ----------------------------------------------------------
CREATE TABLE MOVIMIENTO (
    ID_MOV          NUMBER          DEFAULT SEQ_MOVIMIENTO.NEXTVAL,
    FECHA           DATE            NOT NULL,
    VALOR           NUMBER(15, 2)   NOT NULL,
    CODIGO_DETALLE  VARCHAR2(10)    NOT NULL,
    ID_CUENTA       NUMBER          NOT NULL,
    ID_VOLANTE      NUMBER,
    ID_PERIODO      NUMBER          NOT NULL,
    CONSTRAINT PK_MOVIMIENTO        PRIMARY KEY (ID_MOV),
    CONSTRAINT CK_MOV_VAL           CHECK (VALOR > 0),
    CONSTRAINT FK_MOV_CUENTA        FOREIGN KEY (ID_CUENTA)
        REFERENCES CUENTA_CORRIENTE(ID_CUENTA) ON DELETE CASCADE,
    CONSTRAINT FK_MOV_CODDET        FOREIGN KEY (CODIGO_DETALLE)
        REFERENCES CODIGO_DETALLE(CODIGO_DETALLE),
    CONSTRAINT FK_MOV_VOLANTE       FOREIGN KEY (ID_VOLANTE)
        REFERENCES VOLANTE_MATRICULA(ID_VOLANTE) ON DELETE SET NULL,
    CONSTRAINT FK_MOV_PERIODO       FOREIGN KEY (ID_PERIODO)
        REFERENCES PERIODO_ACADEMICO(ID_PERIODO) ON DELETE CASCADE
);

-- ----------------------------------------------------------
-- 4.18 TRANSACCION_PAGO
-- id_mov NOT NULL UNIQUE: relacion 1:1 con MOVIMIENTO.
-- TRANSACCION_PAGO depende de MOVIMIENTO (no al reves).
-- ----------------------------------------------------------
CREATE TABLE TRANSACCION_PAGO (
    ID_TRANSACCION  NUMBER          DEFAULT SEQ_TRANSACCION.NEXTVAL,
    REFERENCIA      VARCHAR2(100),
    MEDIO_PAGO      VARCHAR2(30),
    FECHA_PAGO      DATE            NOT NULL,
    ID_MOV          NUMBER          NOT NULL,
    CONSTRAINT PK_TRANSACCION       PRIMARY KEY (ID_TRANSACCION),
    CONSTRAINT UQ_TRANS_MOV         UNIQUE (ID_MOV),
    CONSTRAINT FK_TRANS_MOV         FOREIGN KEY (ID_MOV)
        REFERENCES MOVIMIENTO(ID_MOV) ON DELETE CASCADE
);

-- ----------------------------------------------------------
-- 4.19 VOLANTE_MATRICULA_ASIGNATURA
-- Asignaturas de un volante por creditos.
-- CASCADE: si se elimina el volante, sus lineas desaparecen.
-- ----------------------------------------------------------
CREATE TABLE VOLANTE_MATRICULA_ASIGNATURA (
    ID_ASIGNATURA   NUMBER  NOT NULL,
    ID_VOLANTE      NUMBER  NOT NULL,
    CONSTRAINT PK_VMA           PRIMARY KEY (ID_ASIGNATURA, ID_VOLANTE),
    CONSTRAINT FK_VMA_VOLANTE   FOREIGN KEY (ID_VOLANTE)
        REFERENCES VOLANTE_MATRICULA(ID_VOLANTE) ON DELETE CASCADE,
    CONSTRAINT FK_VMA_ASIG      FOREIGN KEY (ID_ASIGNATURA)
        REFERENCES ASIGNATURA(ID_ASIGNATURA) ON DELETE CASCADE
);

PROMPT >>> Tablas creadas. (19 tablas)


-- ============================================================
-- SECCION 5: INDICES
-- ============================================================

PROMPT >>> Creando indices...

CREATE INDEX IDX_MOV_CUENTA       ON MOVIMIENTO(ID_CUENTA);
CREATE INDEX IDX_MOV_PERIODO      ON MOVIMIENTO(ID_PERIODO);
CREATE INDEX IDX_MOV_CODDET       ON MOVIMIENTO(CODIGO_DETALLE);
CREATE INDEX IDX_MOV_VOLANTE      ON MOVIMIENTO(ID_VOLANTE);
CREATE INDEX IDX_VOL_ESTUDIANTE   ON VOLANTE_MATRICULA(ID_ESTUDIANTE);
CREATE INDEX IDX_VOL_PERIODO      ON VOLANTE_MATRICULA(ID_PERIODO);
CREATE INDEX IDX_VOL_PROGRAMA     ON VOLANTE_MATRICULA(ID_PROGRAMA);
CREATE INDEX IDX_EST_PROGRAMA     ON ESTUDIANTE(ID_PROGRAMA);
CREATE INDEX IDX_PEA_PROG_SEM     ON PLAN_ESTUDIO_ASIGNATURA(ID_PROGRAMA, SEMESTRE);
CREATE INDEX IDX_RC_PROG_PER      ON REGLA_COBRO(ID_PROGRAMA, ID_PERIODO);

PROMPT >>> Indices creados. (10 indices)


-- ============================================================
-- SECCION 6: DATOS SEMILLA
-- Los datos semilla estan en entregable4_dml.sql (Seccion 0).
-- Ejecutar el DDL primero y luego el DML.
-- ============================================================

PROMPT >>> Seccion 6 omitida: ejecutar entregable4_dml.sql para insertar datos.

-- (placeholder para mantener numeracion de secciones)
-- Las siguientes secciones continuan normalmente.

-- 6.1 (movido al DML)
-- INSERT INTO PERFIL ...  => ver entregable4_dml.sql Seccion 0


-- ============================================================
-- SECCION 7: TRIGGERS (ENTREGABLE #5)
-- ============================================================

PROMPT >>> Creando triggers...

-- ----------------------------------------------------------
-- TRIGGER 7.1: TR_CREAR_CUENTA_CORRIENTE
-- Crea automaticamente la cuenta corriente al generar
-- el primer volante de un estudiante.
-- ----------------------------------------------------------
CREATE OR REPLACE TRIGGER TR_CREAR_CUENTA_CORRIENTE
BEFORE INSERT ON VOLANTE_MATRICULA
FOR EACH ROW
DECLARE
    v_existe NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_existe
    FROM   CUENTA_CORRIENTE
    WHERE  ID_ESTUDIANTE = :NEW.ID_ESTUDIANTE;

    IF v_existe = 0 THEN
        INSERT INTO CUENTA_CORRIENTE (ID_CUENTA, ID_ESTUDIANTE)
        VALUES (SEQ_CUENTA.NEXTVAL, :NEW.ID_ESTUDIANTE);
    END IF;
END TR_CREAR_CUENTA_CORRIENTE;
/

-- ----------------------------------------------------------
-- TRIGGER 7.2: TR_CALCULAR_MONTO_VOLANTE
-- Calcula MONTO_TOTAL al insertar el volante.
-- GLOBAL   => toma VALORGLOBAL de REGLA_COBRO.
-- CREDITOS => suma creditos del semestre x VALORCREDITO.
-- ----------------------------------------------------------
CREATE OR REPLACE TRIGGER TR_CALCULAR_MONTO_VOLANTE
BEFORE INSERT ON VOLANTE_MATRICULA
FOR EACH ROW
DECLARE
    v_monto     NUMBER(15, 2) := 0;
    v_valglobal REGLA_COBRO.VALORGLOBAL%TYPE;
    v_valcred   REGLA_COBRO.VALORCREDITO%TYPE;
BEGIN
    IF :NEW.MODALIDAD = 'GLOBAL' THEN
        BEGIN
            SELECT VALORGLOBAL INTO v_valglobal
            FROM   REGLA_COBRO
            WHERE  MODALIDAD   = 'GLOBAL'
              AND  ID_PROGRAMA = :NEW.ID_PROGRAMA
              AND  ID_PERIODO  = :NEW.ID_PERIODO;
            v_monto := NVL(v_valglobal, 0);
        EXCEPTION
            WHEN NO_DATA_FOUND THEN v_monto := 0;
            WHEN TOO_MANY_ROWS THEN
                SELECT MAX(VALORGLOBAL) INTO v_monto
                FROM REGLA_COBRO
                WHERE MODALIDAD='GLOBAL'
                  AND ID_PROGRAMA=:NEW.ID_PROGRAMA
                  AND ID_PERIODO=:NEW.ID_PERIODO;
        END;

    ELSIF :NEW.MODALIDAD = 'CREDITOS' THEN
        BEGIN
            SELECT VALORCREDITO INTO v_valcred
            FROM   REGLA_COBRO
            WHERE  MODALIDAD   = 'CREDITOS'
              AND  ID_PROGRAMA = :NEW.ID_PROGRAMA
              AND  ID_PERIODO  = :NEW.ID_PERIODO;

            SELECT NVL(SUM(a.CANT_CREDITOS), 0) * NVL(v_valcred, 0) INTO v_monto
            FROM   PLAN_ESTUDIO_ASIGNATURA pea
            JOIN   ASIGNATURA a ON a.ID_ASIGNATURA = pea.ID_ASIGNATURA
            WHERE  pea.ID_PROGRAMA = :NEW.ID_PROGRAMA
              AND  pea.SEMESTRE    = :NEW.SEMESTRE_QUE_COBRA;
        EXCEPTION
            WHEN NO_DATA_FOUND THEN v_monto := 0;
        END;
    END IF;

    :NEW.MONTO_TOTAL := v_monto;
END TR_CALCULAR_MONTO_VOLANTE;
/

-- ----------------------------------------------------------
-- TRIGGER 7.3: TR_RECALCULAR_MONTO_CREDITOS
-- Recalcula MONTO_TOTAL cuando se agregan o eliminan
-- asignaturas especificas en un volante por creditos.
-- Implementado como COMPOUND TRIGGER para evitar ORA-04091
-- (mutating table): el FOR EACH ROW solo guarda IDs de volante
-- afectados; el AFTER STATEMENT lee la tabla (ya sin mutar)
-- y ejecuta el UPDATE sobre VOLANTE_MATRICULA.
-- ----------------------------------------------------------
CREATE OR REPLACE TRIGGER TR_RECALCULAR_MONTO_CREDITOS
FOR INSERT OR DELETE ON VOLANTE_MATRICULA_ASIGNATURA
COMPOUND TRIGGER

    TYPE t_ids IS TABLE OF NUMBER INDEX BY PLS_INTEGER;
    v_vols t_ids;
    v_cnt  PLS_INTEGER := 0;

    -- Guarda el ID del volante afectado en cada fila procesada
    AFTER EACH ROW IS
    BEGIN
        v_cnt := v_cnt + 1;
        v_vols(v_cnt) := CASE WHEN INSERTING THEN :NEW.ID_VOLANTE
                              ELSE :OLD.ID_VOLANTE END;
    END AFTER EACH ROW;

    -- Una vez finalizada la sentencia, recalcula el monto
    -- (la tabla ya no está en estado mutante)
    AFTER STATEMENT IS
        v_modalidad VOLANTE_MATRICULA.MODALIDAD%TYPE;
        v_valcred   REGLA_COBRO.VALORCREDITO%TYPE;
        v_monto     NUMBER(15, 2);
        v_id        NUMBER;
    BEGIN
        FOR i IN 1 .. v_cnt LOOP
            v_id := v_vols(i);
            BEGIN
                SELECT MODALIDAD INTO v_modalidad
                FROM   VOLANTE_MATRICULA
                WHERE  ID_VOLANTE = v_id;

                IF v_modalidad = 'CREDITOS' THEN
                    SELECT rc.VALORCREDITO INTO v_valcred
                    FROM   VOLANTE_MATRICULA vm
                    JOIN   REGLA_COBRO rc
                           ON  rc.MODALIDAD   = vm.MODALIDAD
                           AND rc.ID_PROGRAMA = vm.ID_PROGRAMA
                           AND rc.ID_PERIODO  = vm.ID_PERIODO
                    WHERE  vm.ID_VOLANTE = v_id;

                    SELECT NVL(SUM(a.CANT_CREDITOS), 0) * v_valcred INTO v_monto
                    FROM   VOLANTE_MATRICULA_ASIGNATURA vma
                    JOIN   ASIGNATURA a ON a.ID_ASIGNATURA = vma.ID_ASIGNATURA
                    WHERE  vma.ID_VOLANTE = v_id;

                    UPDATE VOLANTE_MATRICULA
                    SET    MONTO_TOTAL = v_monto
                    WHERE  ID_VOLANTE  = v_id;
                END IF;
            EXCEPTION
                WHEN NO_DATA_FOUND THEN NULL;
            END;
        END LOOP;
    END AFTER STATEMENT;

END TR_RECALCULAR_MONTO_CREDITOS;
/

-- ----------------------------------------------------------
-- TRIGGER 7.4: TR_ACTUALIZAR_ESTADO_VOLANTE
-- Actualiza ESTADO del volante tras cada movimiento.
-- PENDIENTE => PARCIAL => PAGADO segun cobros vs pagos.
-- Implementado como COMPOUND TRIGGER para evitar ORA-04091
-- (mutating table) al leer MOVIMIENTO desde un trigger
-- de fila sobre la misma tabla.
-- ----------------------------------------------------------
CREATE OR REPLACE TRIGGER TR_ACTUALIZAR_ESTADO_VOLANTE
FOR INSERT ON MOVIMIENTO
COMPOUND TRIGGER
-- Usa coleccion para manejar correctamente inserts masivos.
-- Cada fila guarda su id_volante; el AFTER STATEMENT
-- procesa todos de una vez sin riesgo de ORA-04091.

    TYPE t_volantes IS TABLE OF NUMBER INDEX BY PLS_INTEGER;
    v_volantes  t_volantes;
    v_idx       PLS_INTEGER := 0;

    AFTER EACH ROW IS
        v_duplicado BOOLEAN := FALSE;
    BEGIN
        IF :NEW.ID_VOLANTE IS NOT NULL THEN
            -- Verificar si ya esta en la coleccion para no procesar doble
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
    BEGIN
        NULL; -- El estado se calcula en tiempo de consulta desde VW_SALDO_PERIODO
    END AFTER STATEMENT;

END TR_ACTUALIZAR_ESTADO_VOLANTE;
/

-- ----------------------------------------------------------
-- TRIGGER 7.5: TR_VALIDAR_MOVIMIENTO_CUENTA
-- Verifica que el movimiento se registre en la cuenta
-- correcta del dueno del volante.
-- ----------------------------------------------------------
CREATE OR REPLACE TRIGGER TR_VALIDAR_MOVIMIENTO_CUENTA
BEFORE INSERT ON MOVIMIENTO
FOR EACH ROW
DECLARE
    v_cuenta_volante NUMBER;
BEGIN
    IF :NEW.ID_VOLANTE IS NOT NULL THEN
        SELECT cc.ID_CUENTA INTO v_cuenta_volante
        FROM   VOLANTE_MATRICULA vm
        JOIN   CUENTA_CORRIENTE cc ON cc.ID_ESTUDIANTE = vm.ID_ESTUDIANTE
        WHERE  vm.ID_VOLANTE = :NEW.ID_VOLANTE;

        IF v_cuenta_volante <> :NEW.ID_CUENTA THEN
            RAISE_APPLICATION_ERROR(-20001,
                'La cuenta corriente no corresponde al estudiante del volante.');
        END IF;
    END IF;
END TR_VALIDAR_MOVIMIENTO_CUENTA;
/

-- ----------------------------------------------------------
-- TRIGGER 7.6: TR_RECALCULAR_MONTO_VOLANTE
-- Recalcula MONTO_TOTAL del volante cada vez que se inserta
-- un movimiento de tipo COBRO asociado a ese volante.
-- Cubre cobros adicionales como PCAR, PLAB, PEXA que se
-- agregan después de generar el volante inicial.
-- ----------------------------------------------------------
CREATE OR REPLACE TRIGGER TR_RECALCULAR_MONTO_VOLANTE
FOR INSERT ON MOVIMIENTO
COMPOUND TRIGGER
-- Acumula IDs de volantes con cobros adicionales (PCAR, PLAB, PEXA, etc.)
-- para recalcular MONTO_TOTAL en AFTER STATEMENT sin riesgo de ORA-04091.

    TYPE t_volantes IS TABLE OF NUMBER INDEX BY PLS_INTEGER;
    v_volantes  t_volantes;
    v_idx       PLS_INTEGER := 0;

    AFTER EACH ROW IS
        v_duplicado BOOLEAN := FALSE;
    BEGIN
        IF :NEW.ID_VOLANTE IS NOT NULL THEN
            -- Verificar si el volante ya esta en la coleccion
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
        v_nuevo_monto  NUMBER(15, 2);
        v_grupo        CODIGO_DETALLE.GRUPO%TYPE;
    BEGIN
        FOR i IN 1 .. v_idx LOOP
            -- Solo recalcular si hay al menos un COBRO en el volante
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

-- ----------------------------------------------------------
-- TRIGGER 7.7: TR_BORRAR_VOLANTE_POR_MOVIMIENTO
-- Si se elimina el movimiento de cargo principal (Matricula o Credito),
-- se elimina el volante para permitir volver a generarlo.
-- Usa COMPOUND TRIGGER para evitar ORA-04091: el delete a
-- VOLANTE_MATRICULA se ejecuta en AFTER STATEMENT, cuando
-- MOVIMIENTO ya no esta en estado mutating.
-- ----------------------------------------------------------
CREATE OR REPLACE TRIGGER TR_BORRAR_VOLANTE_POR_MOVIMIENTO
FOR DELETE ON MOVIMIENTO
COMPOUND TRIGGER

    TYPE t_volantes IS TABLE OF NUMBER INDEX BY PLS_INTEGER;
    v_volantes  t_volantes;
    v_idx       PLS_INTEGER := 0;

    BEFORE EACH ROW IS
        v_dup BOOLEAN := FALSE;
    BEGIN
        IF :OLD.ID_VOLANTE IS NOT NULL AND
           (:OLD.CODIGO_DETALLE = 'PMAT' OR :OLD.CODIGO_DETALLE = 'PCRE') THEN
            FOR i IN 1 .. v_idx LOOP
                IF v_volantes(i) = :OLD.ID_VOLANTE THEN
                    v_dup := TRUE;
                    EXIT;
                END IF;
            END LOOP;
            IF NOT v_dup THEN
                v_idx := v_idx + 1;
                v_volantes(v_idx) := :OLD.ID_VOLANTE;
            END IF;
        END IF;
    END BEFORE EACH ROW;

    AFTER STATEMENT IS
    BEGIN
        FOR i IN 1 .. v_idx LOOP
            -- Desvincula cobros adicionales del volante antes de borrarlo
            -- (evita FK violation al intentar borrar VOLANTE_MATRICULA)
            UPDATE MOVIMIENTO
            SET    ID_VOLANTE = NULL
            WHERE  ID_VOLANTE = v_volantes(i);

            DELETE FROM VOLANTE_MATRICULA
            WHERE  ID_VOLANTE = v_volantes(i);
        END LOOP;
    END AFTER STATEMENT;

END TR_BORRAR_VOLANTE_POR_MOVIMIENTO;
/

PROMPT >>> Triggers creados. (7 triggers)

-- ============================================================
-- SECCION 8: VISTAS DE REPORTES (ENTREGABLE #5)
-- ============================================================

PROMPT >>> Creando vistas...

-- ----------------------------------------------------------
-- VISTA 8.0: VW_CONSULTA_PAGOS
-- Consolida transaccion, movimiento y datos del estudiante.
-- ----------------------------------------------------------
CREATE OR REPLACE VIEW VW_CONSULTA_PAGOS AS
SELECT 
    T.ID_TRANSACCION,
    T.REFERENCIA,
    T.MEDIO_PAGO,
    T.FECHA_PAGO,
    M.VALOR AS VALOR_PAGADO,
    M.ID_MOV,
    E.CARNET,
    E.NOMBRE || ' ' || E.APELLIDO AS NOMBRE_ESTUDIANTE,
    CD.DESCRIPCION AS CONCEPTO,
    M.ID_PERIODO
FROM TRANSACCION_PAGO T
JOIN MOVIMIENTO M ON T.ID_MOV = M.ID_MOV
JOIN CUENTA_CORRIENTE C ON M.ID_CUENTA = C.ID_CUENTA
JOIN ESTUDIANTE E ON C.ID_ESTUDIANTE = E.ID_ESTUDIANTE
JOIN CODIGO_DETALLE CD ON M.CODIGO_DETALLE = CD.CODIGO_DETALLE;

-- ----------------------------------------------------------
-- VISTA 8.1: VW_LISTADO_ESTUDIANTES
-- Define el "Monto" como la suma de todos los cobros del periodo.
-- ----------------------------------------------------------
CREATE OR REPLACE VIEW VW_LISTADO_ESTUDIANTES AS
SELECT
    e.ID_ESTUDIANTE,
    e.CARNET,
    e.NOMBRE                        AS NOMBRE_ESTUDIANTE,
    e.APELLIDO                      AS APELLIDO_ESTUDIANTE,
    pa.NOMBRE_PROGRAMA,
    per.NOMBRE_PERIODO,
    MAX(vm.MODALIDAD)               AS MODALIDAD,
    NVL(SUM(CASE WHEN cd.GRUPO = 'COBRO' THEN m.VALOR ELSE 0 END), 0) AS MONTO_TOTAL
FROM   ESTUDIANTE          e
JOIN   PROGRAMA_ACADEMICO  pa  ON pa.ID_PROGRAMA  = e.ID_PROGRAMA
JOIN   CUENTA_CORRIENTE    cc  ON cc.ID_ESTUDIANTE = e.ID_ESTUDIANTE
LEFT JOIN MOVIMIENTO       m   ON m.ID_CUENTA      = cc.ID_CUENTA
LEFT JOIN CODIGO_DETALLE   cd  ON cd.CODIGO_DETALLE = m.CODIGO_DETALLE
LEFT JOIN PERIODO_ACADEMICO per ON per.ID_PERIODO   = m.ID_PERIODO
LEFT JOIN VOLANTE_MATRICULA vm ON vm.ID_ESTUDIANTE = e.ID_ESTUDIANTE AND (vm.ID_PERIODO = m.ID_PERIODO OR m.ID_PERIODO IS NULL)
GROUP BY e.ID_ESTUDIANTE, e.CARNET, e.NOMBRE, e.APELLIDO, pa.NOMBRE_PROGRAMA, per.NOMBRE_PERIODO;

-- ----------------------------------------------------------
-- VISTA 8.2: VW_INGRESO_ESPERADO
-- Ingreso esperado = Suma de todos los COBROS del periodo.
-- ----------------------------------------------------------
CREATE OR REPLACE VIEW VW_INGRESO_ESPERADO AS
SELECT
    per.NOMBRE_PERIODO,
    pa.NOMBRE_PROGRAMA,
    SUM(m.VALOR)                    AS TOTAL_ESPERADO
FROM   MOVIMIENTO          m
JOIN   CODIGO_DETALLE      cd  ON cd.CODIGO_DETALLE = m.CODIGO_DETALLE
JOIN   CUENTA_CORRIENTE    cc  ON cc.ID_CUENTA      = m.ID_CUENTA
JOIN   ESTUDIANTE          e   ON e.ID_ESTUDIANTE   = cc.ID_ESTUDIANTE
JOIN   PROGRAMA_ACADEMICO  pa  ON pa.ID_PROGRAMA    = e.ID_PROGRAMA
JOIN   PERIODO_ACADEMICO   per ON per.ID_PERIODO    = m.ID_PERIODO
WHERE  cd.GRUPO = 'COBRO'
GROUP BY per.NOMBRE_PERIODO, pa.NOMBRE_PROGRAMA;

-- ----------------------------------------------------------
-- VISTA 8.3: VW_PENDIENTES_PAGO
-- Listado de estudiantes con deuda en el periodo.
-- Calcula: Total Cobros - Total Pagos > 0.
-- ----------------------------------------------------------
CREATE OR REPLACE VIEW VW_PENDIENTES_PAGO AS
SELECT
    e.ID_ESTUDIANTE,
    e.CARNET,
    e.NOMBRE                        AS NOMBRE_ESTUDIANTE,
    e.APELLIDO                      AS APELLIDO_ESTUDIANTE,
    e.CORREO,
    e.TELEFONO,
    pa.ID_PROGRAMA,
    pa.NOMBRE_PROGRAMA,
    per.NOMBRE_PERIODO,
    bal.TOTAL_COBRADO,
    bal.TOTAL_PAGADO,
    (bal.TOTAL_COBRADO - bal.TOTAL_PAGADO) AS SALDO_PENDIENTE,
    CASE 
        WHEN bal.TOTAL_PAGADO = 0 THEN 'PENDIENTE'
        ELSE 'PARCIAL'
    END AS ESTADO
FROM (
    SELECT 
        m.ID_CUENTA, 
        m.ID_PERIODO,
        SUM(CASE WHEN cd.GRUPO = 'COBRO' THEN m.VALOR ELSE 0 END) AS TOTAL_COBRADO,
        SUM(CASE WHEN cd.GRUPO = 'PAGO'  THEN m.VALOR ELSE 0 END) AS TOTAL_PAGADO
    FROM MOVIMIENTO m
    JOIN CODIGO_DETALLE cd ON m.CODIGO_DETALLE = cd.CODIGO_DETALLE
    GROUP BY m.ID_CUENTA, m.ID_PERIODO
) bal
JOIN CUENTA_CORRIENTE cc ON bal.ID_CUENTA = cc.ID_CUENTA
JOIN ESTUDIANTE e ON cc.ID_ESTUDIANTE = e.ID_ESTUDIANTE
JOIN PROGRAMA_ACADEMICO pa ON e.ID_PROGRAMA = pa.ID_PROGRAMA
JOIN PERIODO_ACADEMICO per ON bal.ID_PERIODO = per.ID_PERIODO
WHERE (bal.TOTAL_COBRADO - bal.TOTAL_PAGADO) > 0;

-- ----------------------------------------------------------
-- VISTA 8.4: VW_INGRESO_REAL
-- Ingreso Real = Suma de los PAGOS reales del periodo.
-- Se excluye el codigo DESC (Descuento) porque no representa
-- dinero que realmente ingresa a la empresa: solo reduce la
-- deuda del estudiante sin generar un flujo de caja real.
-- ----------------------------------------------------------
CREATE OR REPLACE VIEW VW_INGRESO_REAL AS
SELECT
    per.NOMBRE_PERIODO,
    SUM(m.VALOR)                        AS TOTAL_RECAUDADO
FROM   MOVIMIENTO          m
JOIN   CODIGO_DETALLE      cd  ON cd.CODIGO_DETALLE = m.CODIGO_DETALLE
JOIN   PERIODO_ACADEMICO   per ON per.ID_PERIODO    = m.ID_PERIODO
WHERE  cd.GRUPO = 'PAGO'
  AND  cd.CODIGO_DETALLE != 'DESC'
GROUP BY per.NOMBRE_PERIODO;

-- ----------------------------------------------------------
-- VISTA 8.5: VW_CARTERA
-- ----------------------------------------------------------
CREATE OR REPLACE VIEW VW_CARTERA AS
SELECT
    e.ID_ESTUDIANTE,
    e.CARNET,
    e.NOMBRE                AS NOMBRE_ESTUDIANTE,
    e.APELLIDO              AS APELLIDO_ESTUDIANTE,
    e.CORREO,
    pa.NOMBRE_PROGRAMA,
    per.NOMBRE_PERIODO,
    SUM(m.VALOR)            AS VALOR_CREDITO
FROM   MOVIMIENTO          m
JOIN   CODIGO_DETALLE      cd  ON cd.CODIGO_DETALLE = m.CODIGO_DETALLE
JOIN   CUENTA_CORRIENTE    cc  ON cc.ID_CUENTA      = m.ID_CUENTA
JOIN   ESTUDIANTE          e   ON e.ID_ESTUDIANTE   = cc.ID_ESTUDIANTE
JOIN   PROGRAMA_ACADEMICO  pa  ON pa.ID_PROGRAMA    = e.ID_PROGRAMA
JOIN   PERIODO_ACADEMICO   per ON per.ID_PERIODO    = m.ID_PERIODO
WHERE  cd.CODIGO_DETALLE = 'CRED'
GROUP BY e.ID_ESTUDIANTE, e.CARNET, e.NOMBRE, e.APELLIDO, e.CORREO,
         pa.NOMBRE_PROGRAMA, per.NOMBRE_PERIODO
;

-- ----------------------------------------------------------
-- VISTA 8.6: VW_CUENTA_CORRIENTE_DETALLE
-- Incluye SALDO_ACUMULADO linea por linea usando funcion ventana.
-- ----------------------------------------------------------
CREATE OR REPLACE VIEW VW_CUENTA_CORRIENTE_DETALLE AS
SELECT
    e.ID_ESTUDIANTE,
    e.CARNET,
    e.NOMBRE || ' ' || e.APELLIDO                       AS NOMBRE_COMPLETO,
    pa.NOMBRE_PROGRAMA,
    per.NOMBRE_PERIODO,
    m.ID_MOV,
    m.FECHA,
    m.CODIGO_DETALLE,
    cd.DESCRIPCION                                      AS DESCRIPCION_MOVIMIENTO,
    cd.GRUPO,
    CASE cd.GRUPO WHEN 'COBRO' THEN m.VALOR ELSE NULL END   AS DEBITO,
    CASE cd.GRUPO WHEN 'PAGO'  THEN m.VALOR ELSE NULL END   AS CREDITO,
    SUM(
        CASE cd.GRUPO
            WHEN 'COBRO' THEN  m.VALOR
            WHEN 'PAGO'  THEN -m.VALOR
        END
    ) OVER (
        PARTITION BY cc.ID_CUENTA, m.ID_PERIODO
        ORDER BY m.FECHA, m.ID_MOV
    )                                                   AS SALDO_ACUMULADO
FROM   MOVIMIENTO          m
JOIN   CODIGO_DETALLE      cd  ON cd.CODIGO_DETALLE = m.CODIGO_DETALLE
JOIN   CUENTA_CORRIENTE    cc  ON cc.ID_CUENTA      = m.ID_CUENTA
JOIN   ESTUDIANTE          e   ON e.ID_ESTUDIANTE   = cc.ID_ESTUDIANTE
JOIN   PROGRAMA_ACADEMICO  pa  ON pa.ID_PROGRAMA    = e.ID_PROGRAMA
JOIN   PERIODO_ACADEMICO   per ON per.ID_PERIODO    = m.ID_PERIODO
;

-- ----------------------------------------------------------
-- VISTA 8.7: VW_SALDO_PERIODO
-- Balance total por estudiante y periodo.
-- Implementa la regla COBROS - PAGOS = 0.
-- ----------------------------------------------------------
CREATE OR REPLACE VIEW VW_SALDO_PERIODO AS
SELECT
    e.ID_ESTUDIANTE,
    e.NOMBRE || ' ' || e.APELLIDO                       AS ESTUDIANTE,
    per.ID_PERIODO,
    per.NOMBRE_PERIODO,
    SUM(CASE WHEN cd.GRUPO = 'COBRO' THEN m.VALOR ELSE 0 END)  AS TOTAL_COBROS,
    SUM(CASE WHEN cd.GRUPO = 'PAGO'  THEN m.VALOR ELSE 0 END)  AS TOTAL_PAGOS,
    SUM(CASE
        WHEN cd.GRUPO = 'COBRO' THEN  m.VALOR
        WHEN cd.GRUPO = 'PAGO'  THEN -m.VALOR
    END)                                                AS SALDO_NETO
FROM   MOVIMIENTO          m
JOIN   CUENTA_CORRIENTE    cc  ON m.ID_CUENTA       = cc.ID_CUENTA
JOIN   ESTUDIANTE          e   ON cc.ID_ESTUDIANTE  = e.ID_ESTUDIANTE
JOIN   CODIGO_DETALLE      cd  ON m.CODIGO_DETALLE  = cd.CODIGO_DETALLE
JOIN   PERIODO_ACADEMICO   per ON m.ID_PERIODO      = per.ID_PERIODO
GROUP BY e.ID_ESTUDIANTE, e.NOMBRE, e.APELLIDO,
         per.ID_PERIODO, per.NOMBRE_PERIODO
;

PROMPT >>> Vistas creadas. (8 vistas)


COMMIT;
PROMPT ==============================================
PROMPT   SCRIPT COMPLETO EJECUTADO EXITOSAMENTE
PROMPT   Entregable #3: 19 tablas | 12 secuencias
PROMPT                  10 indices
PROMPT   Entregable #4: datos semilla insertados
PROMPT   Entregable #5: 5 triggers | 7 vistas
PROMPT ==============================================


-- ============================================================
-- SECCION 9: VERIFICACION
-- Ejecutar despues del script completo para confirmar
-- que todo se creo correctamente.
-- ============================================================

PROMPT ============================================
PROMPT  1. TABLAS (esperado: 19)
PROMPT ============================================
SELECT TABLE_NAME
FROM   USER_TABLES
WHERE  TABLE_NAME IN (
    'PERFIL','MENU','PERMISO','PROGRAMA_ACADEMICO',
    'PERIODO_ACADEMICO','ASIGNATURA','CODIGO_DETALLE',
    'PERSONA','PERFIL_PERMISO','USUARIO','REGLA_COBRO',
    'PLAN_ESTUDIO','ESTUDIANTE','PLAN_ESTUDIO_ASIGNATURA',
    'CUENTA_CORRIENTE','VOLANTE_MATRICULA','MOVIMIENTO',
    'TRANSACCION_PAGO','VOLANTE_MATRICULA_ASIGNATURA'
)
ORDER BY TABLE_NAME;

PROMPT ============================================
PROMPT  2. SECUENCIAS (esperado: 12)
PROMPT ============================================
SELECT SEQUENCE_NAME, LAST_NUMBER AS SIGUIENTE_VALOR
FROM   USER_SEQUENCES
WHERE  SEQUENCE_NAME IN (
    'SEQ_PERFIL','SEQ_MENU','SEQ_PERMISO','SEQ_USUARIO',
    'SEQ_PROGRAMA','SEQ_PERIODO','SEQ_ASIGNATURA',
    'SEQ_ESTUDIANTE','SEQ_CUENTA','SEQ_VOLANTE',
    'SEQ_MOVIMIENTO','SEQ_TRANSACCION'
)
ORDER BY SEQUENCE_NAME;

PROMPT ============================================
PROMPT  3. INDICES MANUALES (esperado: 10)
PROMPT ============================================
SELECT INDEX_NAME, TABLE_NAME
FROM   USER_INDEXES
WHERE  INDEX_NAME IN (
    'IDX_MOV_CUENTA','IDX_MOV_PERIODO','IDX_MOV_CODDET',
    'IDX_MOV_VOLANTE','IDX_VOL_ESTUDIANTE','IDX_VOL_PERIODO',
    'IDX_VOL_PROGRAMA','IDX_EST_PROGRAMA',
    'IDX_PEA_PROG_SEM','IDX_RC_PROG_PER'
)
ORDER BY TABLE_NAME, INDEX_NAME;

PROMPT ============================================
PROMPT  4. CONSTRAINTS (STATUS debe ser ENABLED)
PROMPT ============================================
SELECT TABLE_NAME, CONSTRAINT_NAME, CONSTRAINT_TYPE, STATUS
FROM   USER_CONSTRAINTS
WHERE  STATUS = 'DISABLED'
  AND  CONSTRAINT_TYPE IN ('P','R','U','C');
-- Si no devuelve filas, todos los constraints estan habilitados.

PROMPT ============================================
PROMPT  5. TRIGGERS (esperado: 7, STATUS: ENABLED)
PROMPT ============================================
SELECT TRIGGER_NAME, TABLE_NAME, STATUS
FROM   USER_TRIGGERS
WHERE  TRIGGER_NAME IN (
    'TR_CREAR_CUENTA_CORRIENTE',
    'TR_CALCULAR_MONTO_VOLANTE',
    'TR_RECALCULAR_MONTO_CREDITOS',
    'TR_ACTUALIZAR_ESTADO_VOLANTE',
    'TR_VALIDAR_MOVIMIENTO_CUENTA',
    'TR_RECALCULAR_MONTO_VOLANTE',
    'TR_BORRAR_VOLANTE_POR_MOVIMIENTO'
)
ORDER BY TABLE_NAME, TRIGGER_NAME;

PROMPT ============================================
PROMPT  6. VISTAS (esperado: 7)
PROMPT ============================================
SELECT VIEW_NAME
FROM   USER_VIEWS
WHERE  VIEW_NAME IN (
    'VW_LISTADO_ESTUDIANTES','VW_INGRESO_ESPERADO',
    'VW_PENDIENTES_PAGO','VW_INGRESO_REAL',
    'VW_CARTERA','VW_CUENTA_CORRIENTE_DETALLE',
    'VW_SALDO_PERIODO'
)
ORDER BY VIEW_NAME;

PROMPT ============================================
PROMPT  7. CONTEO DE DATOS SEMILLA
PROMPT ============================================
SELECT *
FROM (
    SELECT 'PERFIL'                     AS TABLA, COUNT(*) AS FILAS FROM PERFIL              UNION ALL
    SELECT 'MENU',                                COUNT(*)           FROM MENU                UNION ALL
    SELECT 'PERMISO',                             COUNT(*)           FROM PERMISO             UNION ALL
    SELECT 'PERFIL_PERMISO',                      COUNT(*)           FROM PERFIL_PERMISO      UNION ALL
    SELECT 'CODIGO_DETALLE',                      COUNT(*)           FROM CODIGO_DETALLE      UNION ALL
    SELECT 'PROGRAMA_ACADEMICO',                  COUNT(*)           FROM PROGRAMA_ACADEMICO  UNION ALL
    SELECT 'PERIODO_ACADEMICO',                   COUNT(*)           FROM PERIODO_ACADEMICO   UNION ALL
    SELECT 'ASIGNATURA',                          COUNT(*)           FROM ASIGNATURA          UNION ALL
    SELECT 'PLAN_ESTUDIO',                        COUNT(*)           FROM PLAN_ESTUDIO        UNION ALL
    SELECT 'PLAN_ESTUDIO_ASIGNATURA',             COUNT(*)           FROM PLAN_ESTUDIO_ASIGNATURA UNION ALL
    SELECT 'REGLA_COBRO',                         COUNT(*)           FROM REGLA_COBRO         UNION ALL
    SELECT 'PERSONA',                             COUNT(*)           FROM PERSONA             UNION ALL
    SELECT 'USUARIO',                             COUNT(*)           FROM USUARIO             UNION ALL
    SELECT 'ESTUDIANTE',                          COUNT(*)           FROM ESTUDIANTE          UNION ALL
    SELECT 'CUENTA_CORRIENTE',                    COUNT(*)           FROM CUENTA_CORRIENTE    UNION ALL
    SELECT 'VOLANTE_MATRICULA',                   COUNT(*)           FROM VOLANTE_MATRICULA   UNION ALL
    SELECT 'MOVIMIENTO',                          COUNT(*)           FROM MOVIMIENTO          UNION ALL
    SELECT 'TRANSACCION_PAGO',                    COUNT(*)           FROM TRANSACCION_PAGO    UNION ALL
    SELECT 'VOLANTE_MATRICULA_ASIGNATURA',        COUNT(*)           FROM VOLANTE_MATRICULA_ASIGNATURA
)
ORDER BY TABLA;

PROMPT ============================================
PROMPT  8. PERMISOS POR PERFIL
PROMPT  (ADMINISTRADOR: 16, SUPERVISOR: 6, ASISTENTE: 5)
PROMPT ============================================
SELECT p.NOMBRE_PERFIL, COUNT(pp.ID_PERMISO) AS TOTAL_PERMISOS
FROM   PERFIL p
LEFT JOIN PERFIL_PERMISO pp ON pp.ID_PERFIL = p.ID_PERFIL
GROUP BY p.ID_PERFIL, p.NOMBRE_PERFIL
ORDER BY p.NOMBRE_PERFIL;

PROMPT ============================================
PROMPT  9. PRUEBA FUNCIONAL - COBRO GLOBAL
PROMPT  Verifica: TR_CREAR_CUENTA_CORRIENTE y
PROMPT  TR_CALCULAR_MONTO_VOLANTE.
PROMPT  Esperado: MONTO_TOTAL=8500000, cuenta corriente creada
PROMPT ============================================

-- Datos temporales autocontenidos (no dependen del DML)
-- Codigos de detalle de prueba
INSERT INTO CODIGO_DETALLE VALUES ('T_COB', 'COBRO', 'Cobro prueba DDL', NULL);
INSERT INTO CODIGO_DETALLE VALUES ('T_PAG', 'PAGO',  'Pago prueba DDL',  NULL);
-- Programa y periodo de prueba
INSERT INTO PROGRAMA_ACADEMICO (ID_PROGRAMA, NOMBRE_PROGRAMA, CODIGO_PROGRAMA)
    VALUES (99999, '_TEST_DDL_', 'TST');
INSERT INTO PERIODO_ACADEMICO (ID_PERIODO, NOMBRE_PERIODO, FECHA_INICIO, FECHA_FIN)
    VALUES (99999, '_TEST_DDL_', DATE '2026-01-01', DATE '2026-06-30');
-- Plan de estudio (semestre 1) y regla de cobro GLOBAL = 8.500.000
INSERT INTO PLAN_ESTUDIO (SEMESTRE, ID_PROGRAMA)
    SELECT 1, ID_PROGRAMA FROM PROGRAMA_ACADEMICO WHERE NOMBRE_PROGRAMA = '_TEST_DDL_';
INSERT INTO REGLA_COBRO (MODALIDAD, VALORCREDITO, VALORGLOBAL, ID_PROGRAMA, ID_PERIODO)
    SELECT 'GLOBAL', NULL, 8500000, p.ID_PROGRAMA, per.ID_PERIODO
    FROM   PROGRAMA_ACADEMICO p CROSS JOIN PERIODO_ACADEMICO per
    WHERE  p.NOMBRE_PROGRAMA = '_TEST_DDL_' AND per.NOMBRE_PERIODO = '_TEST_DDL_';
-- Estudiante de prueba (sin FK a PERSONA)
INSERT INTO ESTUDIANTE (ID_ESTUDIANTE, CARNET, NOMBRE, APELLIDO, TELEFONO, CORREO, ID_PROGRAMA)
    SELECT 99999, '_TEST_DDL_', 'Test', 'DDL',
           '0000000000', 'test@ddl.test', ID_PROGRAMA
    FROM   PROGRAMA_ACADEMICO WHERE NOMBRE_PROGRAMA = '_TEST_DDL_';
COMMIT;

-- Insertar volante: TR_CREAR_CUENTA_CORRIENTE crea la cuenta y
-- TR_CALCULAR_MONTO_VOLANTE fija MONTO_TOTAL=8500000
INSERT INTO VOLANTE_MATRICULA
    (ID_VOLANTE, SEMESTRE_QUE_COBRA, TIPO_GENERACION, ID_ESTUDIANTE, ID_PERIODO, MODALIDAD, ID_PROGRAMA)
    SELECT 99999, 1, 'INDIVIDUAL',
           e.ID_ESTUDIANTE, per.ID_PERIODO, 'GLOBAL', p.ID_PROGRAMA
    FROM   ESTUDIANTE         e
    JOIN   PROGRAMA_ACADEMICO p   ON p.ID_PROGRAMA   = e.ID_PROGRAMA
    CROSS JOIN PERIODO_ACADEMICO per
    WHERE  e.CARNET = '_TEST_DDL_' AND per.NOMBRE_PERIODO = '_TEST_DDL_';
COMMIT;

SELECT v.ID_VOLANTE,
       e.NOMBRE || ' ' || e.APELLIDO       AS ESTUDIANTE,
       v.MODALIDAD,
       v.MONTO_TOTAL,
       NVL(TO_CHAR(cc.ID_CUENTA),'SIN CUENTA') AS CUENTA_CREADA
FROM   VOLANTE_MATRICULA   v
JOIN   ESTUDIANTE          e  ON e.ID_ESTUDIANTE  = v.ID_ESTUDIANTE
LEFT JOIN CUENTA_CORRIENTE cc ON cc.ID_ESTUDIANTE = v.ID_ESTUDIANTE
WHERE  e.CARNET = '_TEST_DDL_';

PROMPT ============================================
PROMPT  10. PRUEBA FUNCIONAL - PAGO PARCIAL
PROMPT  Verifica: TR_ACTUALIZAR_ESTADO_VOLANTE.
PROMPT  Esperado: SALDO_NETO = 4500000 (PARCIAL)
PROMPT ============================================

-- Cobro: usa subquery para ID_CUENTA e ID_VOLANTE reales
INSERT INTO MOVIMIENTO (ID_MOV, FECHA, VALOR, CODIGO_DETALLE, ID_CUENTA, ID_VOLANTE, ID_PERIODO)
    SELECT SEQ_MOVIMIENTO.NEXTVAL, SYSDATE, 8500000, 'T_COB',
           cc.ID_CUENTA, v.ID_VOLANTE, v.ID_PERIODO
    FROM   VOLANTE_MATRICULA  v
    JOIN   CUENTA_CORRIENTE   cc ON cc.ID_ESTUDIANTE = v.ID_ESTUDIANTE
    JOIN   ESTUDIANTE          e  ON e.ID_ESTUDIANTE  = v.ID_ESTUDIANTE
    WHERE  e.CARNET = '_TEST_DDL_';

-- Pago parcial (4.000.000 < cobro 8.500.000) => PARCIAL
INSERT INTO MOVIMIENTO (ID_MOV, FECHA, VALOR, CODIGO_DETALLE, ID_CUENTA, ID_VOLANTE, ID_PERIODO)
    SELECT SEQ_MOVIMIENTO.NEXTVAL, SYSDATE, 4000000, 'T_PAG',
           cc.ID_CUENTA, v.ID_VOLANTE, v.ID_PERIODO
    FROM   VOLANTE_MATRICULA  v
    JOIN   CUENTA_CORRIENTE   cc ON cc.ID_ESTUDIANTE = v.ID_ESTUDIANTE
    JOIN   ESTUDIANTE          e  ON e.ID_ESTUDIANTE  = v.ID_ESTUDIANTE
    WHERE  e.CARNET = '_TEST_DDL_';

-- Transaccion de pago (referencia al movimiento PAGO via subquery)
INSERT INTO TRANSACCION_PAGO (ID_TRANSACCION, REFERENCIA, MEDIO_PAGO, FECHA_PAGO, ID_MOV)
    SELECT SEQ_TRANSACCION.NEXTVAL, 'REF-DDL-TEST', 'EFECTIVO', SYSDATE, m.ID_MOV
    FROM   MOVIMIENTO        m
    JOIN   CUENTA_CORRIENTE  cc ON cc.ID_CUENTA      = m.ID_CUENTA
    JOIN   ESTUDIANTE         e  ON e.ID_ESTUDIANTE   = cc.ID_ESTUDIANTE
    WHERE  e.CARNET = '_TEST_DDL_' AND m.CODIGO_DETALLE = 'T_PAG';
COMMIT;

SELECT v.ID_VOLANTE,
       e.NOMBRE || ' ' || e.APELLIDO AS ESTUDIANTE,
       v.MONTO_TOTAL,
       sp.TOTAL_COBROS,
       sp.TOTAL_PAGOS,
       sp.SALDO_NETO,
       CASE
           WHEN sp.SALDO_NETO <= 0                        THEN 'PAGADO'
           WHEN sp.TOTAL_PAGOS > 0 AND sp.SALDO_NETO > 0  THEN 'PARCIAL'
           ELSE                                                 'PENDIENTE'
       END AS ESTADO_CALCULADO
FROM   VOLANTE_MATRICULA  v
JOIN   ESTUDIANTE          e   ON e.ID_ESTUDIANTE  = v.ID_ESTUDIANTE
JOIN   VW_SALDO_PERIODO    sp  ON sp.ID_ESTUDIANTE = e.ID_ESTUDIANTE
WHERE  e.CARNET = '_TEST_DDL_';

PROMPT ============================================
PROMPT  11. BALANCE CUENTA CORRIENTE
PROMPT  Esperado: COBROS=8500000, PAGOS=4000000,
PROMPT  SALDO_NETO=4500000
PROMPT ============================================

SELECT ESTUDIANTE, NOMBRE_PERIODO,
       TOTAL_COBROS, TOTAL_PAGOS, SALDO_NETO
FROM   VW_SALDO_PERIODO
WHERE  ESTUDIANTE LIKE 'Test DDL%';

-- Limpieza de datos de prueba (CASCADE elimina dependientes)
PROMPT >>> Limpiando datos temporales de prueba DDL...
DELETE FROM TRANSACCION_PAGO
WHERE  ID_MOV IN (
    SELECT m.ID_MOV FROM MOVIMIENTO m
    JOIN   CUENTA_CORRIENTE cc ON cc.ID_CUENTA = m.ID_CUENTA
    JOIN   ESTUDIANTE e ON e.ID_ESTUDIANTE = cc.ID_ESTUDIANTE
    WHERE  e.CARNET = '_TEST_DDL_'
);
DELETE FROM MOVIMIENTO
WHERE  ID_CUENTA IN (
    SELECT cc.ID_CUENTA FROM CUENTA_CORRIENTE cc
    JOIN   ESTUDIANTE e ON e.ID_ESTUDIANTE = cc.ID_ESTUDIANTE
    WHERE  e.CARNET = '_TEST_DDL_'
);
DELETE FROM VOLANTE_MATRICULA
WHERE  ID_ESTUDIANTE IN (SELECT ID_ESTUDIANTE FROM ESTUDIANTE WHERE CARNET = '_TEST_DDL_');
DELETE FROM CUENTA_CORRIENTE
WHERE  ID_ESTUDIANTE IN (SELECT ID_ESTUDIANTE FROM ESTUDIANTE WHERE CARNET = '_TEST_DDL_');
DELETE FROM ESTUDIANTE WHERE CARNET = '_TEST_DDL_';
DELETE FROM REGLA_COBRO
WHERE  ID_PERIODO  IN (SELECT ID_PERIODO  FROM PERIODO_ACADEMICO  WHERE NOMBRE_PERIODO  = '_TEST_DDL_')
   AND ID_PROGRAMA IN (SELECT ID_PROGRAMA FROM PROGRAMA_ACADEMICO WHERE NOMBRE_PROGRAMA = '_TEST_DDL_');
DELETE FROM PLAN_ESTUDIO
WHERE  ID_PROGRAMA IN (SELECT ID_PROGRAMA FROM PROGRAMA_ACADEMICO WHERE NOMBRE_PROGRAMA = '_TEST_DDL_');
DELETE FROM PERIODO_ACADEMICO  WHERE NOMBRE_PERIODO  = '_TEST_DDL_';
DELETE FROM PROGRAMA_ACADEMICO WHERE NOMBRE_PROGRAMA = '_TEST_DDL_';
DELETE FROM CODIGO_DETALLE WHERE CODIGO_DETALLE IN ('T_COB','T_PAG');
COMMIT;

PROMPT ==============================================
PROMPT   Verificacion completada.
PROMPT   Los datos de prueba han sido eliminados.
PROMPT   El DDL esta listo. Ejecute el DML a continuacion.
PROMPT ==============================================