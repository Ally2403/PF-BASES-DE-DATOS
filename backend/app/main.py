"""
main.py — Punto de entrada de la aplicación FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import auth, supervisor, administrador

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
# REGISTRAR RUTAS
# =============================================
app.include_router(auth.router)
app.include_router(supervisor.router)
app.include_router(administrador.router)

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

@app.get("/", tags=["Root"])
async def root():
    """
    Mensaje de bienvenida.
    """
    return {
        "message": "Bienvenido a la API de Cuenta Corriente del Estudiante",
        "docs": "/docs",
        "version": "1.0.0"
    }

# =============================================
# RUTAS (se importarán en etapas posteriores)
# Estructura:
#   - app/routes/auth.py → POST /api/auth/login ✅ (Etapa 3)
#   - app/routes/supervisor.py → CRUD de datos base ✅ (Etapa 4)
#   - app/routes/admin.py → Gestión de usuarios y perfiles (Etapa 5)
#   - app/routes/asistente.py → Gestión de cobros (Etapa 6)
#   - app/routes/reportes.py → Reportes desde vistas (Etapa 8)
# =============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
