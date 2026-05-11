# Backend API — Cuenta Corriente del Estudiante

## 📋 Estructura del Proyecto

```
backend/
├── Dockerfile              # Imagen Docker del backend
├── requirements.txt        # Dependencias Python
├── tests/                  # Scripts de prueba por etapa
└── app/
    ├── __init__.py
    ├── main.py            # Aplicación FastAPI principal
    ├── config.py          # Configuración (variables de entorno)
    ├── routes/            # Endpoints de la API
    │   ├── auth.py        # Etapa 3: POST /api/auth/login
    │   ├── supervisor.py  # Etapa 4: CRUD datos base
    │   ├── administrador.py # Etapa 5: Gestión usuarios/perfiles
    │   ├── asistente.py   # Etapa 6: Cobros y pagos
    │   ├── cuenta_corriente.py # Etapa 7: Cuenta corriente
    │   └── reportes.py    # Etapa 8: Reportes desde vistas
    ├── services/          # Lógica de negocio y conexión BD
    │   ├── database.py    # Conexión Oracle (oracledb)
    │   ├── auth.py        # Autenticación SHA-256 + JWT
    │   ├── permissions.py # Control de permisos por perfil
    │   ├── programa.py, asignatura.py, ... # CRUD por entidad
    │   ├── volante.py     # Lógica de volantes de matrícula
    │   ├── movimiento.py  # Cobros adicionales, pagos, eliminación
    │   ├── cuenta_corriente.py # Consultas a VW_CUENTA_CORRIENTE_*
    │   └── reportes.py    # Consultas a vistas de reportes
    └── schemas/           # Esquemas Pydantic (validación)

docker-compose.yml         # Orquestación: backend + Oracle
.env                       # Variables de entorno (secreto, no subir)
```

---

## 🚀 Cómo levantar el proyecto

### Requisitos previos:
1. **Docker** instalado
2. **Oracle corriendo en Docker** en la red `universidad-net`:
   ```bash
   docker network create universidad-net
   
   docker run -d \
     --name oracle-universidad \
     --network universidad-net \
     -p 1522:1521 \
     -e ORACLE_PASSWORD=Admin1234 \
     -e APP_USER=app_user \
     -e APP_USER_PASSWORD=AppPass1234 \
     -v oracle-universidad-data:/opt/oracle/oradata \
     gvenzl/oracle-xe
   ```
3. **Verificar que Oracle esté listo**:
   ```bash
   docker logs -f oracle-universidad
   # Esperar a ver: "DATABASE IS READY TO USE!"
   ```
4. **Ejecutar el DDL** (una sola vez):
   ```bash
   # Conectarse como app_user y ejecutar el script
   docker exec -i oracle-universidad sqlplus app_user/AppPass1234@//localhost:1521/XEPDB1 < entregable3_ddl_final_final.sql
   ```

### Levantar el backend localmente
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### La API estará en:
- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

---

## 📡 Endpoints del Sistema

### Autenticación (Etapa 3)
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/auth/login` | Login con username + password, retorna JWT |

### CRUD Datos Base — SUPERVISOR (Etapa 4)
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET/POST | `/api/programas` | Programas académicos |
| GET/POST | `/api/asignaturas` | Asignaturas |
| GET/POST | `/api/periodos` | Períodos académicos |
| GET/POST | `/api/estudiantes` | Estudiantes |
| PUT | `/api/estudiantes/{id}` | Editar estudiante |
| GET/POST | `/api/programas/{id}/planes` | Planes de estudio |
| GET/POST | `/api/programas/{id}/planes/{sem}/asignaturas` | Asignaturas del plan |
| GET/POST | `/api/programas/{id}/periodos/{id}/reglas` | Reglas de cobro |
| GET/POST | `/api/codigos` | Códigos de detalle |

### Gestión de Usuarios — ADMINISTRADOR (Etapa 5)
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET/POST | `/api/personas` | Personas (datos civiles) |
| GET/POST | `/api/usuarios` | Usuarios del sistema |
| GET/POST | `/api/perfiles` | Perfiles con permisos |
| GET/POST | `/api/menus` | Menús del sistema |

### Lógica de Cobro — ASISTENTE (Etapa 6)
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/asistente/volantes` | Listar volantes |
| GET | `/api/asistente/volantes/{id}` | Detalle de un volante |
| POST | `/api/asistente/volantes/individual` | Generar volante individual |
| POST | `/api/asistente/volantes/masiva` | Generar volantes masivos |
| GET | `/api/asistente/volantes/{id}/movimientos` | Movimientos de un volante |
| POST | `/api/asistente/cobros-adicionales` | Agregar cobro (PCAR, PLAB, PEXA) |
| POST | `/api/asistente/pagos` | Registrar pago |
| DELETE | `/api/asistente/movimientos/{id}` | Eliminar movimiento |

### Cuenta Corriente (Etapa 7)
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/cuenta-corriente/{id_estudiante}` | Detalle completo (VW_CUENTA_CORRIENTE_DETALLE) |
| GET | `/api/cuenta-corriente/{id_estudiante}/saldo` | Saldo por periodo (VW_SALDO_PERIODO) |

### Reportes (Etapa 8)
| Método | Ruta | Vista Oracle |
|--------|------|-------------|
| GET | `/api/reportes/listado-estudiantes` | VW_LISTADO_ESTUDIANTES |
| GET | `/api/reportes/ingreso-esperado` | VW_INGRESO_ESPERADO |
| GET | `/api/reportes/pendientes-pago?id_programa={id}` | VW_PENDIENTES_PAGO |
| GET | `/api/reportes/ingreso-real` | VW_INGRESO_REAL |
| GET | `/api/reportes/cartera` | VW_CARTERA |
| GET | `/api/reportes/consulta-pagos` | VW_CONSULTA_PAGOS |

---

## 🔒 Perfiles y Permisos

| Perfil | Acceso |
|--------|--------|
| **ADMINISTRADOR** | Todo el sistema |
| **SUPERVISOR** | Programas, asignaturas, estudiantes, reglas, códigos, reportes |
| **ASISTENTE** | Volantes, cobros, pagos, cuenta corriente, reportes |

---

## ⚙️ Triggers de Oracle (lógica en BD)

| Trigger | Función |
|---------|---------|
| `TR_CREAR_CUENTA_CORRIENTE` | Crea cuenta al primer volante del estudiante |
| `TR_CALCULAR_MONTO_VOLANTE` | Calcula monto GLOBAL o por CREDITOS |
| `TR_RECALCULAR_MONTO_CREDITOS` | Recalcula al agregar/quitar asignaturas |
| `TR_ACTUALIZAR_ESTADO_VOLANTE` | PENDIENTE → PARCIAL → PAGADO |
| `TR_VALIDAR_MOVIMIENTO_CUENTA` | Verifica movimiento en cuenta correcta |
| `TR_RECALCULAR_MONTO_VOLANTE` | Recalcula al insertar cobros adicionales |
| `TR_BORRAR_VOLANTE_POR_MOVIMIENTO` | Borra volante si se elimina cobro principal |

> **Importante:** El backend NO duplica esta lógica — solo inserta/consulta y deja que Oracle ejecute los triggers.

---

## 🧪 Usuarios de prueba

| Username | Password | Perfil |
|----------|----------|--------|
| `cmendoza` | `password123` | ADMINISTRADOR |
| `aperez` | `password123` | SUPERVISOR |
| `ltorres` | `password123` | ASISTENTE |

---

## 💡 Stack Tecnológico

- **Python** + **FastAPI** — Framework web
- **oracledb** (python-oracledb) — Driver de Oracle (modo thin)
- **JWT** (python-jose) — Autenticación
- **Pydantic v2** — Validación de datos
- **Docker** + **Docker Compose** — Contenedores
- **Oracle XE** (gvenzl/oracle-xe) — Base de datos

