"""
main.py — Punto de entrada de la aplicación FastAPI
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse
from app.config import settings
from app.routes import auth, supervisor, administrador, asistente
from app.routes import cuenta_corriente, reportes
import logging
import os

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# =============================================
# CREAR APLICACIÓN FASTAPI
# =============================================
app = FastAPI(
    title="API Cuenta Corriente del Estudiante",
    description="Backend para gestión de cobros y pagos de matrículas",
    version="1.0.0",
    debug=settings.debug
)

# =============================================
# CONFIGURAR CORS
# Para que el frontend de la compañera pueda consumir la API
# =============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================
# MANEJO GLOBAL DE ERRORES (Etapa 9)
# =============================================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Captura excepciones no manejadas y retorna JSON consistente."""
    logger.error(f"✗ Error no manejado en {request.method} {request.url}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": f"Error interno del servidor: {str(exc)}",
            "data": None
        }
    )


# =============================================
# REGISTRAR RUTAS PRIMERO
# =============================================
# Etapa 3 — Autenticación
app.include_router(auth.router)
# Etapa 4 — CRUD de entidades base (SUPERVISOR)
app.include_router(supervisor.router)
# Etapa 5 — Gestión de usuarios (ADMINISTRADOR)
app.include_router(administrador.router)
# Etapa 6 — Lógica de cobro (ASISTENTE)
app.include_router(asistente.router)
# Etapa 7 — Cuenta corriente
app.include_router(cuenta_corriente.router)
# Etapa 8 — Reportes
app.include_router(reportes.router)

# =============================================
# CONFIGURAR ARCHIVOS ESTÁTICOS (FRONTEND)
# Se monta DESPUÉS de las rutas para que /api/* tenga precedencia
# =============================================
# Ruta a la carpeta frontend (relativa a este archivo o absoluta)
frontend_path = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
    logger.info(f"✓ Archivos estáticos servidos desde: {frontend_path}")
else:
    logger.warning(f"⚠ Carpeta frontend no encontrada en: {frontend_path}")

# =============================================
# HEALTH CHECK - VERIFICAR QUE LA API ESTÁ VIVA
# =============================================
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Endpoint para verificar que la API está corriendo.
    Útil para Docker Compose y health checks.
    """
    return {
        "status": "ok",
        "environment": settings.environment,
        "service": "backend-universidad"
    }

@app.get("/", tags=["Root"], include_in_schema=False)
async def root():
    """Redirige al login."""
    return RedirectResponse(url="/login.html")

# =============================================
# RUTAS REGISTRADAS:
#   - app/routes/auth.py            → POST /api/auth/login              ✅ (Etapa 3)
#   - app/routes/supervisor.py      → CRUD de datos base                ✅ (Etapa 4)
#   - app/routes/administrador.py   → Gestión de usuarios y perfiles    ✅ (Etapa 5)
#   - app/routes/asistente.py       → Gestión de cobros y pagos         ✅ (Etapa 6)
#   - app/routes/cuenta_corriente.py→ Cuenta corriente del estudiante   ✅ (Etapa 7)
#   - app/routes/reportes.py        → Reportes desde vistas Oracle      ✅ (Etapa 8)
# =============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
