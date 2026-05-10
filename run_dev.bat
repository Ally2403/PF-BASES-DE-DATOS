@echo off
REM run_dev.bat - Script para levantar la API en desarrollo

echo.
echo ============================================================
echo Levantando API - Cuenta Corriente del Estudiante
echo ============================================================
echo.

cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
