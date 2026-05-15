"""
services/email_service.py — Envío de correos via SMTP (Outlook/Hotmail)
"""

import smtplib
import string
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings
import logging

logger = logging.getLogger(__name__)


def generar_contrasena_temporal(longitud: int = 10) -> str:
    """Genera una contraseña temporal aleatoria de letras y dígitos."""
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=longitud))


def enviar_credenciales(correo_destino: str, nombre: str, username: str, nueva_contrasena: str) -> None:
    """
    Envía un correo con las credenciales de acceso al usuario.
    Lanza excepción si falla el envío.
    """
    if not settings.smtp_user or not settings.smtp_pass:
        raise RuntimeError(
            "SMTP no configurado. Complete SMTP_USER y SMTP_PASS en el archivo .env"
        )

    asunto = "Sus credenciales de acceso al Sistema Universitario"

    cuerpo_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: auto;">
        <h2 style="color: #1a3a5c;">Sistema de Gestión Universitaria</h2>
        <p>Estimado/a <strong>{nombre}</strong>,</p>
        <p>A continuación encontrará sus credenciales de acceso al sistema:</p>
        <table style="border-collapse: collapse; width: 100%; margin: 16px 0;">
            <tr>
                <td style="padding: 10px; background: #f0f4f8; font-weight: bold; border: 1px solid #ccc; width: 40%;">Usuario</td>
                <td style="padding: 10px; border: 1px solid #ccc; font-size: 1.1em;">{username}</td>
            </tr>
            <tr>
                <td style="padding: 10px; background: #f0f4f8; font-weight: bold; border: 1px solid #ccc;">Contraseña temporal</td>
                <td style="padding: 10px; border: 1px solid #ccc; font-size: 1.1em; font-family: monospace; letter-spacing: 2px;">{nueva_contrasena}</td>
            </tr>
        </table>
        <p style="color: #c0392b;"><strong>Importante:</strong> Esta es una contraseña temporal generada automáticamente.
        Por seguridad, le recomendamos cambiarla al iniciar sesión.</p>
        <hr style="border: none; border-top: 1px solid #ddd; margin: 24px 0;" />
        <p style="font-size: 0.85em; color: #888;">Este mensaje fue generado automáticamente. No responda a este correo.</p>
    </body>
    </html>
    """

    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = asunto
    mensaje["From"] = settings.smtp_from or settings.smtp_user
    mensaje["To"] = correo_destino
    mensaje.attach(MIMEText(cuerpo_html, "html", "utf-8"))

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as servidor:
            servidor.ehlo()
            servidor.starttls()
            servidor.ehlo()
            servidor.login(settings.smtp_user, settings.smtp_pass)
            servidor.sendmail(settings.smtp_from or settings.smtp_user, correo_destino, mensaje.as_string())
        logger.info(f"✓ Correo de credenciales enviado a {correo_destino}")
    except smtplib.SMTPAuthenticationError:
        logger.error("✗ Error de autenticación SMTP. Verifique SMTP_USER y SMTP_PASS en .env")
        raise RuntimeError("Error de autenticación SMTP. Verifique las credenciales en el archivo .env.")
    except smtplib.SMTPException as e:
        logger.error(f"✗ Error SMTP al enviar correo: {e}")
        raise RuntimeError(f"Error al enviar correo: {e}")
