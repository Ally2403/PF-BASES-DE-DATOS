"""
config.py — Configuración centralizada de la aplicación
Lee variables de entorno desde .env usando pydantic-settings
"""

from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

class Settings(BaseSettings):
    """
    Configuración de la aplicación.
    Lee automáticamente desde .env usando pydantic_settings.
    """
    
    # =============================================
    # BASE DE DATOS ORACLE
    # =============================================
    db_host: str = "oracle-universidad"
    db_port: int = 1521
    db_service: str = "XEPDB1"
    db_user: str = "app_user"
    db_password: str
    
    # =============================================
    # JWT - AUTENTICACIÓN
    # =============================================
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # =============================================
    # CORREO (SMTP)
    # =============================================
    smtp_host: str = "smtp-mail.outlook.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_pass: str = ""
    smtp_from: str = ""

    # =============================================
    # GENERAL
    # =============================================
    environment: str = "development"
    debug: bool = True
    
    class Config:
        # Buscar .env en la raíz del proyecto (padre de backend/)
        env_file = str(Path(__file__).parent.parent.parent / ".env")
        case_sensitive = False

# Instancia global de configuración
settings = Settings()
