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

    asunto = "🎓 Tus credenciales de acceso — Sistema Universitario"

    cuerpo_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
<body style="margin:0;padding:0;background-color:#eef2f7;font-family:'Segoe UI',Arial,sans-serif;">

  <!-- Wrapper -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#eef2f7;padding:32px 0;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">

          <!-- ── HEADER ── -->
          <tr>
            <td style="background:linear-gradient(135deg,#1a3a5c 0%,#2563a8 100%);
                        border-radius:12px 12px 0 0;padding:36px 40px;text-align:center;">
              <div style="display:inline-block;background:rgba(255,255,255,.15);
                          border-radius:50%;width:64px;height:64px;line-height:64px;
                          font-size:32px;margin-bottom:14px;">🎓</div>
              <h1 style="margin:0;color:#ffffff;font-size:22px;font-weight:700;
                          letter-spacing:.5px;">Sistema de Gestión Universitaria</h1>
              <p style="margin:6px 0 0;color:rgba(255,255,255,.75);font-size:13px;">
                Acceso al Portal Académico
              </p>
            </td>
          </tr>

          <!-- ── BODY ── -->
          <tr>
            <td style="background:#ffffff;padding:36px 40px;">

              <p style="margin:0 0 6px;font-size:18px;font-weight:600;color:#1a3a5c;">
                ¡Hola, {nombre}! 👋
              </p>
              <p style="margin:0 0 24px;font-size:14px;color:#555;line-height:1.6;">
                Tu contraseña ha sido restablecida.
                A continuación encontrarás tus credenciales para ingresar al sistema.
              </p>

              <!-- Credentials card -->
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="background:#f4f8ff;border:1px solid #d0e0f7;
                            border-radius:10px;margin-bottom:24px;overflow:hidden;">
                <tr>
                  <td style="padding:20px 24px;border-bottom:1px solid #d0e0f7;">
                    <p style="margin:0 0 4px;font-size:11px;text-transform:uppercase;
                               letter-spacing:1px;color:#7a9abb;font-weight:600;">
                      Usuario
                    </p>
                    <p style="margin:0;font-size:20px;font-weight:700;color:#1a3a5c;
                               letter-spacing:.5px;">
                      {username}
                    </p>
                  </td>
                </tr>
                <tr>
                  <td style="padding:20px 24px;">
                    <p style="margin:0 0 4px;font-size:11px;text-transform:uppercase;
                               letter-spacing:1px;color:#7a9abb;font-weight:600;">
                      Contraseña temporal
                    </p>
                    <p style="margin:0;font-size:24px;font-weight:700;color:#2563a8;
                               font-family:'Courier New',monospace;letter-spacing:4px;">
                      {nueva_contrasena}
                    </p>
                  </td>
                </tr>
              </table>

              <!-- Warning box -->
              <table width="100%" cellpadding="0" cellspacing="0"
                     style="background:#fff8e1;border-left:4px solid #f59e0b;
                            border-radius:0 8px 8px 0;margin-bottom:28px;">
                <tr>
                  <td style="padding:14px 18px;">
                    <p style="margin:0;font-size:13px;color:#78350f;line-height:1.6;">
                      <strong>⚠️ Contraseña temporal:</strong> Por seguridad te recomendamos
                      contactar con el administrador para cambiar esta contraseña. No la compartas con nadie.
                    </p>
                  </td>
                </tr>
              </table>

              <!-- CTA hint -->
              <p style="margin:0;font-size:13px;color:#666;line-height:1.6;">
                Si no solicitaste este acceso o crees que es un error, comunícate de inmediato
                con el administrador del sistema.
              </p>

            </td>
          </tr>

          <!-- ── FOOTER ── -->
          <tr>
            <td style="background:#f0f4f8;border-radius:0 0 12px 12px;
                        padding:20px 40px;text-align:center;border-top:1px solid #dce8f5;">
              <p style="margin:0;font-size:11px;color:#9aa8bb;line-height:1.7;">
                Este mensaje fue generado automáticamente · No respondas a este correo<br/>
                &copy; 2026 Sistema de Gestión Universitaria
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>

</body>
</html>"""

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
