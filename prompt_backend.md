# Prompt para construir el backend — Proyecto Cuenta Corriente del Estudiante

---

Hola. Voy a adjuntarte varios archivos de un proyecto universitario de bases de datos. Necesito que me ayudes a construir el backend en Python paso a paso. Lee todo con atención antes de escribir cualquier código.

---

## Archivos adjuntos

Te estoy entregando los siguientes archivos — léelos todos antes de empezar:

1. **`PROYECTO_FINAL_202610.md`** — Documento con las instrucciones completas del proyecto: reglas de negocio, perfiles de usuario (ADMINISTRADOR, SUPERVISOR, ASISTENTE), reportes requeridos y casos especiales.
2. **`entregable3_ddl_final_final.sql`** — Script DDL completo de Oracle con 19 tablas, 12 secuencias, 10 índices, **7 triggers** y 8 vistas. **Este es el modelo de datos que debes respetar al 100%.**
3. **`ENTREGABLES_1_Y_2.drawio`** — Archivo con dos diagramas: el **Modelo Entidad-Relación (MER)** y el **Modelo Relacional**. Úsalos para entender la estructura y las relaciones entre entidades. Si no puedes abrir el .drawio directamente, trabaja con el DDL que tiene toda la misma información en SQL.
4. **`ddl_guide.html`** — Guía visual de referencia del modelo de datos.

---

## Contexto del proyecto

El sistema se llama **Cuenta Corriente del Estudiante**. Es un sistema de gestión de cobros y pagos de matrículas para una universidad privada colombiana.

El proyecto está dividido en dos partes:
- **Backend**: me toca a mí — Python, API REST, conexión a Oracle. **Esto es lo único que debes construir.**
- **Frontend**: le toca a mi compañera — ella consumirá los endpoints que yo construya desde su aplicación. **No hagas nada de frontend.**

---

## Cosas importantes del DDL que debes conocer

El DDL tiene **7 triggers** que ya implementan lógica de negocio en la base de datos — el backend NO debe duplicar esta lógica, solo insertar/consultar y dejar que Oracle haga el trabajo:

| Trigger | Qué hace |
|---|---|
| `TR_CREAR_CUENTA_CORRIENTE` | Crea la cuenta corriente automáticamente al generar el primer volante de un estudiante |
| `TR_CALCULAR_MONTO_VOLANTE` | Calcula el `MONTO_TOTAL` del volante al insertarlo (GLOBAL o CREDITOS) |
| `TR_RECALCULAR_MONTO_CREDITOS` | Recalcula el monto cuando se agregan/quitan asignaturas en un volante por créditos |
| `TR_ACTUALIZAR_ESTADO_VOLANTE` | Actualiza el estado del volante (PENDIENTE → PARCIAL → PAGADO) tras cada movimiento |
| `TR_VALIDAR_MOVIMIENTO_CUENTA` | Valida que el movimiento pertenezca a la cuenta correcta del estudiante |
| `TR_RECALCULAR_MONTO_VOLANTE` | Recalcula el `MONTO_TOTAL` cuando se insertan cobros adicionales (PCAR, PLAB, PEXA) después de generar el volante |
| `TR_BORRAR_VOLANTE_POR_MOVIMIENTO` | Si se elimina el movimiento principal (PMAT o PCRE), borra el volante automáticamente para permitir regenerarlo |

El DDL también tiene **8 vistas** (`VW_*`) que ya implementan todos los reportes — úsalas directamente con `SELECT * FROM VW_...` desde el backend.

---

## Stack tecnológico

- **Lenguaje**: Python
- **Framework**: FastAPI
- **Base de datos**: Oracle corriendo en Docker local (imagen `gvenzl/oracle-xe`)
- **Driver Oracle**: `oracledb` (python-oracledb, el driver moderno de Oracle para Python)
- **Contenedores**: Docker + Docker Compose
- **Autenticación**: JWT (JSON Web Tokens)

---

## Configuración de Docker — YA HECHA

La base de datos Oracle ya está corriendo en Docker. El contenedor fue creado con estos comandos:

```bash
# 1. Crear la red interna para que backend y BD se comuniquen
docker network create universidad-net

# 2. Levantar Oracle con gvenzl/oracle-xe
docker run -d \
  --name oracle-universidad \
  --network universidad-net \
  -p 1522:1521 \
  -e ORACLE_PASSWORD=Admin1234 \
  -e APP_USER=app_user \
  -e APP_USER_PASSWORD=AppPass1234 \
  -v oracle-universidad-data:/opt/oracle/oradata \
  gvenzl/oracle-xe

# 3. Verificar que el contenedor esté corriendo y listo
docker logs -f oracle-universidad
# Esperar hasta ver: "DATABASE IS READY TO USE!"
```

Los datos de conexión que debe usar el backend son:
- **Host**: `oracle-universidad` (nombre del contenedor, dentro de la red Docker) o `localhost` (si el backend corre fuera de Docker)
- **Puerto**: `1522` (desde fuera de Docker) / `1521` (entre contenedores dentro de la red Docker)
- **Service name**: `XEPDB1`
- **Usuario de app**: `app_user`
- **Contraseña de app**: `AppPass1234`
- **Usuario admin** (solo para correr el DDL): `system` / `Admin1234`

> **Nota**: el DDL debe ejecutarse conectado como `app_user` una sola vez, para que todas las tablas queden en su schema y puedan consultarse sin prefijo. Los endpoints del backend también usan `app_user`.

---

## Lo que quiero construir

Una API REST en Python (FastAPI) que:

1. Se conecte a Oracle corriendo en Docker local.
2. Exponga endpoints para todas las operaciones del sistema.
3. Maneje autenticación con JWT y respete los tres perfiles: ADMINISTRADOR, SUPERVISOR y ASISTENTE.
4. Aproveche los triggers y vistas ya definidos en el DDL — no dupliques lógica de BD.
5. Esté lista para ser consumida por el frontend de mi compañera vía HTTP (JSON).

---

## Instrucciones de trabajo — MUY IMPORTANTE

**Trabaja paso a paso. No me des todo el proyecto de golpe.**

Avanza en este orden exacto, una etapa a la vez. **Espera mi confirmación** ("está bien, continúa" o "corrígeme esto") antes de pasar a la siguiente etapa. Explícame brevemente qué estás haciendo y por qué en cada paso, para que yo pueda entender y aprender.

### Etapa 1 — Estructura del proyecto y Docker Compose

Crea la estructura de carpetas del backend y los archivos de configuración:

- `docker-compose.yml` que levante el backend (FastAPI) y lo conecte a la red `universidad-net` donde ya está corriendo Oracle. **No levantes Oracle en el Compose — ya está corriendo por separado.**
- `backend/Dockerfile` para el contenedor del backend.
- `backend/requirements.txt` con todas las dependencias necesarias.
- La estructura base de carpetas: `routes/`, `services/`, `models/`, `config.py`, `main.py`.
- Un archivo `.env` con las variables de entorno (credenciales de BD, secret JWT, etc.).
- Un archivo `.env.example` igual pero sin valores reales (para subir al repositorio).

Explícame qué hace cada archivo y cómo levantar el backend con un solo comando.

### Etapa 2 — Conexión a la base de datos

- Escribe el módulo de conexión a Oracle usando `oracledb` (python-oracledb).
- Crea un script de prueba (`test_conexion.py`) que se conecte y haga un `SELECT 1 FROM DUAL` para verificar que todo funciona.
- Explícame cómo probar que la conexión está bien antes de continuar.

### Etapa 3 — Autenticación y perfiles

- Implementa el endpoint `POST /api/auth/login` que reciba `username` y `password`, valide contra la tabla `USUARIO` (la contraseña está almacenada como hash SHA-256) y devuelva un token JWT.
- El token debe incluir el perfil del usuario (ADMINISTRADOR, SUPERVISOR, ASISTENTE) y su `ID_USER`.
- Crea un sistema de dependencias de FastAPI para proteger los endpoints según el perfil requerido.
- Explícame cómo probar el login con curl o Postman.

### Etapa 4 — CRUD de entidades base (SUPERVISOR)

Implementa los endpoints para las entidades que gestiona el SUPERVISOR, una entidad a la vez:
- `PROGRAMA_ACADEMICO` — listar, crear.
- `ASIGNATURA` — listar, crear.
- `PERIODO_ACADEMICO` — listar, crear.
- `PLAN_ESTUDIO` y `PLAN_ESTUDIO_ASIGNATURA` — asignar asignaturas a un semestre de un programa.
- `REGLA_COBRO` — crear reglas por periodo, programa y modalidad (GLOBAL o CREDITOS).
- `CODIGO_DETALLE` — listar, crear.
- `ESTUDIANTE` — listar, crear, editar.

Para cada entidad: dime qué vas a hacer, escribe el código, dime cómo probarlo.

### Etapa 5 — Gestión de usuarios (ADMINISTRADOR)

- `PERSONA` y `USUARIO` — crear usuario, asignar perfil, listar usuarios.
- `PERFIL` y `PERFIL_PERMISO` — listar perfiles con sus permisos.
- `MENU` — listar menús disponibles según perfil del usuario autenticado.

### Etapa 6 — Lógica de cobro (ASISTENTE)

Esta es la parte más importante del sistema:
- `POST /api/volantes/individual` — genera un volante individual. Recibe: `id_estudiante`, `id_periodo`, `modalidad` (GLOBAL o CREDITOS), `semestre_que_cobra`. El trigger `TR_CALCULAR_MONTO_VOLANTE` calcula el monto automáticamente.
- `POST /api/volantes/masiva` — genera volantes para todos los estudiantes de un programa en un periodo.
- `POST /api/cobros-adicionales` — inserta un movimiento de tipo COBRO (PCAR, PLAB, PEXA, etc.) sobre un volante existente. El trigger `TR_RECALCULAR_MONTO_VOLANTE` recalculará el monto automáticamente.
- `POST /api/pagos` — registra un pago. Primero inserta en `MOVIMIENTO` (con `CODIGO_DETALLE` de grupo PAGO, ej: `MPAG`), luego inserta en `TRANSACCION_PAGO` con el `ID_MOV` generado. **Importante:** `TRANSACCION_PAGO` NO tiene columna `VALOR_PAGADO` — el valor del pago vive en `MOVIMIENTO.VALOR`. El trigger `TR_ACTUALIZAR_ESTADO_VOLANTE` actualiza el estado del volante automáticamente.
- `DELETE /api/movimientos/{id_mov}` — elimina un movimiento. Si era el cobro principal (PMAT o PCRE), el trigger `TR_BORRAR_VOLANTE_POR_MOVIMIENTO` elimina el volante automáticamente, permitiendo regenerarlo.

### Etapa 7 — Cuenta corriente

- `GET /api/cuenta-corriente/{id_estudiante}` — devuelve el detalle completo usando la vista `VW_CUENTA_CORRIENTE_DETALLE`.
- `GET /api/cuenta-corriente/{id_estudiante}/saldo` — devuelve el saldo del periodo usando `VW_SALDO_PERIODO`.

### Etapa 8 — Reportes

Endpoints de reportes usando las vistas ya creadas en Oracle:
- `GET /api/reportes/listado-estudiantes` → `VW_LISTADO_ESTUDIANTES`
- `GET /api/reportes/ingreso-esperado` → `VW_INGRESO_ESPERADO`
- `GET /api/reportes/pendientes-pago?id_programa={id}` → `VW_PENDIENTES_PAGO` filtrada por programa
- `GET /api/reportes/ingreso-real` → `VW_INGRESO_REAL`
- `GET /api/reportes/cartera` → `VW_CARTERA`
- `GET /api/reportes/consulta-pagos` → `VW_CONSULTA_PAGOS` (consolida transacciones, movimientos y datos del estudiante)

### Etapa 9 — Detalles finales

- Manejo global de errores (excepciones de Oracle, validaciones de negocio).
- CORS configurado para que el frontend de mi compañera pueda consumir la API.
- Verificar que la documentación automática de FastAPI en `/docs` muestre todos los endpoints.
- `README.md` con instrucciones claras de cómo levantar el proyecto completo.

---

## Reglas que debes seguir

1. **Una etapa a la vez.** No adelantes etapas sin que yo te lo pida.
2. **Explícame qué hace cada archivo o función importante** — quiero entender, no solo copiar.
3. **No hagas nada de frontend.** Ni HTML, ni CSS, ni JavaScript de interfaz.
4. **Aprovecha los 7 triggers y 8 vistas de Oracle.** No dupliques lógica que ya está en la BD.
5. **Usa variables de entorno** para todo lo sensible. Nunca hardcodees credenciales.
6. **Los endpoints deben responder siempre en JSON** con estructura consistente: `{ "data": ..., "message": "...", "success": true/false }`.
7. **Valida los permisos por perfil** — si un ASISTENTE intenta acceder a un endpoint de ADMINISTRADOR, debe recibir un 403.
8. **Si algo no está claro, pregúntame antes de inventarte algo.**

---

Empieza por la **Etapa 1**. Explícame qué vas a crear y luego muéstrame los archivos.
