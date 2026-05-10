# run_dev.ps1 - Script PowerShell para levantar la API en desarrollo

Write-Host ""
Write-Host "============================================================"
Write-Host "Levantando API - Cuenta Corriente del Estudiante"
Write-Host "============================================================"
Write-Host ""

Set-Location backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
