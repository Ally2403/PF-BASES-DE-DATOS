# 📚 Cuenta Corriente del Estudiante
### IST7111 — Bases de Datos 2026-10 | NRC 2076

Sistema de gestión de cobros y pagos de matrículas para una universidad privada colombiana. Permite gestionar estudiantes, programas académicos, volantes de matrícula, pagos y reportes financieros.

---

## 🧰 Requisitos previos

Antes de ejecutar el proyecto, asegúrate de tener instalado lo siguiente en tu computador:

### 1. Docker Desktop
Es el único requisito principal. Docker se encarga de levantar la base de datos y el backend automáticamente.

- Descarga: https://www.docker.com/products/docker-desktop
- Versión mínima recomendada: **4.0 o superior**
- ⚠️ Después de instalarlo, **ábrelo y espera a que el ícono de Docker en la barra de tareas deje de mostrar "Starting..."** antes de continuar.

### 2. Git
Para clonar el repositorio.

- Descarga: https://git-scm.com/downloads
- Durante la instalación, deja todas las opciones por defecto.

### 3. Oracle SQL Developer *(solo si quieres explorar la base de datos)*
No es obligatorio para ejecutar el proyecto, pero útil si quieres hacer consultas directamente a la base de datos.

- Descarga: https://www.oracle.com/tools/downloads/sqldev-downloads.html

---

## 🖥️ Compatibilidad

| Sistema Operativo | Compatible |
|---|---|
| Windows 10/11 | ✅ |
| macOS | ✅ |
| Linux (Ubuntu/Debian) | ✅ |

---

## 🚀 Instalación y ejecución paso a paso

### Paso 1 — Clonar el repositorio

Abre una terminal (Git Bash en Windows, Terminal en Mac/Linux) y ejecuta:

```bash
git clone https://github.com/Ally2403/PF-BASES-DE-DATOS.git
```

Entra a la carpeta del proyecto:

```bash
cd PF-BASES-DE-DATOS
```

---

### Paso 2 — Crear la red interna de Docker

Este comando crea la red que permite que el backend y la base de datos se comuniquen entre sí:

```bash
docker network create universidad-net
```

> ⚠️ Si te dice `Error response from daemon: network with name universidad-net already exists`, no te preocupes — significa que ya existe y puedes continuar sin problema.

---

### Paso 3 — Levantar la base de datos Oracle

Ejecuta este comando para descargar y levantar Oracle XE en Docker:

```bash
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

> ⏳ La primera vez que ejecutes esto, Docker descargará la imagen de Oracle XE (aproximadamente 2 GB). Dependiendo de tu conexión puede tardar entre 5 y 15 minutos.

Luego monitorea el progreso con:

```bash
docker logs -f oracle-universidad
```

**Espera hasta ver este mensaje en la consola:**
```
DATABASE IS READY TO USE!
```

Una vez aparezca, presiona `Ctrl+C` para salir del log. La base de datos seguirá corriendo en segundo plano.

---

### Paso 4 — Cargar el esquema de la base de datos

Ahora debes ejecutar el script DDL que crea todas las tablas, secuencias, triggers, vistas y datos iniciales.

**Opción A — Desde SQL Developer (recomendado):**

1. Abre Oracle SQL Developer
2. Crea una nueva conexión con estos datos:
   - **Connection Name:** `Universidad Docker`
   - **Username:** `app_user`
   - **Password:** `AppPass1234`
   - **Connection Type:** `Basic`
   - **Host:** `localhost`
   - **Port:** `1522`
   - **Service name:** `XEPDB1` *(asegúrate de seleccionar "Service name" y NO "SID")*
3. Haz clic en **Test** — debe decir `Success`
4. Haz clic en **Connect**
5. Ve a **File → Open** y abre el archivo `entregable3_ddl_final_final.sql` que está en la raíz del proyecto
6. Presiona **F5** para ejecutar todo el script
7. Verifica que en el panel de output no haya errores en rojo

**Opción B — Desde la terminal:**

```bash
docker exec -i oracle-universidad sqlplus app_user/AppPass1234@XEPDB1 < entregable3_ddl_final_final.sql
```

---

### Paso 5 — Levantar el backend

Desde la raíz del proyecto ejecuta:

```bash
docker compose up --build
```

Este comando:
1. Construye la imagen del backend con todo el código Python
2. Levanta el servidor FastAPI en el puerto 8000
3. Conecta el backend a la base de datos Oracle automáticamente

Espera hasta ver algo como:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

---

### Paso 6 — Abrir la aplicación

Abre tu navegador y ve a:

```
http://localhost:8000
```

Serás redirigido al login del sistema.

---

## 👤 Usuarios de prueba

El sistema viene con 3 usuarios de prueba precargados:

| Usuario | Contraseña | Perfil |
|---|---|---|
| `cmendoza` | `password123` | ADMINISTRADOR |
| `aperez` | `password123` | SUPERVISOR |
| `ltorres` | `password123` | ASISTENTE |

---

## 🔌 Conexión a la base de datos *(para SQL Developer)*

Si quieres explorar la base de datos directamente:

| Campo | Valor |
|---|---|
| Host | `localhost` |
| Puerto | `1522` |
| Service name | `XEPDB1` |
| Usuario | `app_user` |
| Contraseña | `AppPass1234` |

---

## 📋 Comandos útiles del día a día

```bash
# Levantar todo el proyecto
docker start oracle-universidad
docker compose up

# Parar el backend
docker compose down

# Parar la base de datos
docker stop oracle-universidad

# Ver logs del backend en tiempo real
docker compose logs -f backend

# Ver logs de Oracle
docker logs -f oracle-universidad

# Reconstruir el backend después de cambios en el código
docker compose up --build

# Ver contenedores corriendo
docker ps
```

---

## 🗂️ Estructura del proyecto

```
PF-BASES-DE-DATOS/
│
├── backend/                         ← API REST en Python/FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routes/
│   │   ├── services/
│   │   └── models/
│   └── requirements.txt
│
├── frontend/                        ← Interfaz web en HTML/CSS/JS
│
├── Dockerfile                       ← Construcción de la imagen Docker
├── docker-compose.yml               ← Orquestación de contenedores
├── .env                             ← Variables de entorno
├── entregable3_ddl_final_final.sql  ← Esquema de la base de datos
├── ENTREGABLES_1_Y_2.drawio         ← Diagramas MER y Modelo Relacional
├── PROYECTO_FINAL_202610.docx       ← Documento del proyecto
└── README.md
```

---

## ⚙️ Variables de entorno

El backend usa un archivo `.env` para la configuración. Ya viene incluido en el repositorio con los valores correctos para Docker. Si necesitas recrearlo:

**En Mac/Linux:**
```bash
cp .env.example .env
```

**En Windows:**
```bash
copy .env.example .env
```

Los valores por defecto ya están configurados para funcionar con el Docker del proyecto.

---

## ❓ Solución de problemas frecuentes

**"DATABASE IS READY TO USE!" nunca aparece**
- La primera vez puede tardar hasta 10 minutos. Ten paciencia.
- Verifica que Docker Desktop esté corriendo (ícono en la barra de tareas).

**Error al conectar SQL Developer: "The Network Adapter could not establish the connection"**
- Verifica que el contenedor Oracle esté corriendo: `docker ps`
- Si no aparece, inícialo: `docker start oracle-universidad`

**Error "network universidad-net not found" al levantar el backend**
- Ejecuta primero: `docker network create universidad-net`

**El puerto 1522 ya está en uso**
- Algún otro proceso está usando ese puerto. Intenta reiniciar Docker Desktop.

**"No such container: oracle-universidad"**
- Vuelve al Paso 3 y ejecuta el `docker run` nuevamente.

---

## 📡 API Documentation

Una vez el proyecto esté corriendo, puedes ver la documentación interactiva de todos los endpoints en:

```
http://localhost:8000/docs
```

---

## 📝 Notas técnicas

- La base de datos Oracle XE corre en el puerto **1522** (externo) mapeado al **1521** interno del contenedor.
- El backend se conecta a Oracle usando el service name **XEPDB1**.
- Todas las tablas y objetos de la BD viven en el schema del usuario **app_user**.
- Las contraseñas se almacenan como hash **SHA-256**.
