# README — Backend API Cuenta Corriente del Estudiante

## 📋 Estructura del Proyecto

```
backend/
├── Dockerfile              # Imagen Docker del backend
├── requirements.txt        # Dependencias Python
└── app/
    ├── __init__.py
    ├── main.py            # Aplicación FastAPI principal
    ├── config.py          # Configuración (variables de entorno)
    ├── routes/            # Endpoints de la API (etapas 3-8)
    ├── services/          # Lógica de negocio y conexión BD (etapa 2)
    ├── models/            # Modelos de datos (acceso a BD)
    └── schemas/           # Esquemas Pydantic (validación)

docker-compose.yml         # Orquestación: backend + Oracle
.env                       # Variables de entorno (secreto, no subir)
.env.example              # Template de .env (sin valores reales)
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

### OPCIÓN 1: Con script bash/PowerShell (recomendado)

**PowerShell (Windows):**
```powershell
cd c:\Users\juanp\Desktop\PF Bases
.\run_dev.ps1
```

**CMD (Windows):**
```cmd
cd c:\Users\juanp\Desktop\PF Bases
run_dev.bat
```

### OPCIÓN 2: Comando directo

**Desde la raíz del proyecto:**
```bash
cd c:\Users\juanp\Desktop\PF Bases\backend
python -m uvicorn app.main:app --reload
```

**O desde cualquier lado:**
```bash
cd c:\Users\juanp\Desktop\PF Bases
python -m uvicorn app.main:app --reload --app-dir backend
```

### La API estará en:
- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc
- **Health check**: http://localhost:8000/health

---

## 📝 Archivos de configuración

### `.env` (NO subir a repositorio)
Contiene credenciales reales de BD, secret JWT, etc.

```
DB_HOST=oracle-universidad
DB_PORT=1521
DB_SERVICE=XEPDB1
DB_USER=app_user
DB_PASSWORD=AppPass1234
JWT_SECRET_KEY=tu_clave_muy_segura_min_32_caracteres
```

### `.env.example` (SÍ subir a repositorio)
Template sin valores reales, para que otros sepan qué configurar.

---

## 🔧 Qué hace cada archivo

### `main.py` (Aplicación FastAPI)
- Crea la aplicación FastAPI
- Configura CORS para que el frontend pueda consumir la API
- Health check (`/health`) para verificar que el backend está vivo
- Importará rutas de las etapas 3-8

### `config.py` (Configuración centralizada)
- Lee variables del archivo `.env` automáticamente
- Usa `pydantic_settings` para validación de tipos
- Instancia global `settings` que se importa en toda la app

### `Dockerfile` (Imagen del contenedor)
- Base: `python:3.10-slim`
- Instala gcc (necesario para compilar oracledb)
- Copia requirements e instala dependencias
- Expone puerto 8000

### `docker-compose.yml` (Orquestación)
- Servicio `backend`: levanta la API en puerto 8000
- Variables de entorno mapeadas desde `.env`
- Red: conecta a `universidad-net` donde Oracle corre
- Volume: mapea `./backend` (live reload en desarrollo)
- Comando: `uvicorn` con `--reload` para desarrollo

---

## 📦 Dependencias (requirements.txt)

| Paquete | Versión | Para qué |
|---------|---------|---------|
| FastAPI | 0.104.1 | Framework web |
| uvicorn | 0.24.0 | Servidor ASGI |
| pydantic | 2.5.0 | Validación de datos |
| python-dotenv | 1.0.0 | Leer `.env` (DEPRECATED, ya no se usa con pydantic-settings) |
| python-jose | 3.3.0 | JWT tokens |
| passlib | 1.7.4 | Hash de contraseñas |
| oracledb | 1.4.1 | **Driver de Oracle** (python-oracledb) |
| pydantic-settings | 2.1.0 | Leer variables de entorno |

---

## 🔗 Endpoints base (ETAPA 1)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Mensaje de bienvenida |
| GET | `/health` | Health check (OK si API está viva) |
| GET | `/docs` | Documentación interactiva Swagger |
| GET | `/redoc` | Documentación ReDoc |

---

## 📡 Próximas etapas

### Etapa 2: Conexión a BD
- `app/services/database.py` → Módulo de conexión a Oracle con oracledb
- `test_conexion.py` → Script de prueba SELECT 1 FROM DUAL

### Etapa 3: Autenticación
- `app/routes/auth.py` → POST /api/auth/login
- `app/schemas/auth.py` → LoginRequest, LoginResponse
- `app/services/auth.py` → Lógica de validación y generación de JWT

### Etapas 4-8: CRUD y reportes
- Rutas para cada entidad (programas, estudiantes, volantes, etc.)
- Servicios para cada operación
- Esquemas de validación

---

## 🧪 Verificar que todo funciona

Después de levantarlo:

1. **Health check**:
   ```bash
   curl http://localhost:8000/health
   ```
   Debe retornar: `{"status":"ok","environment":"development","service":"backend-universidad"}`

2. **Ver documentación Swagger**:
   Ir a http://localhost:8000/docs en el navegador

3. **Logs del contenedor**:
   ```bash
   docker-compose logs -f backend
   ```

---

## 💡 Notas

- El backend está configurado con `--reload` para desarrollo, detecta cambios automáticamente
- CORS está abierto (`allow_origins=["*"]`), en producción especificar dominios exactos
- Todas las variables sensibles están en `.env`, nunca se hardcodean
- La BD no se levanta en Docker Compose, ya corre por separado

