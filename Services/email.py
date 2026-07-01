import os
import resend

# La API key se configura como variable de entorno (ver .env)
resend.api_key = os.getenv("RESEND_API_KEY")

# URL del frontend, para construir el enlace de restablecimiento
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Remitente. En el plan gratuito de Resend, mientras no verifiques tu propio
# dominio, solo puedes usar "onboarding@resend.dev" como remitente.
EMAIL_FROM = os.getenv("EMAIL_FROM", "Jaye <onboarding@resend.dev>")


def send_password_reset_email(to_email: str, token: str) -> None:
    """
    Envía el correo de "olvidé mi contraseña" con un enlace que contiene
    el token (no exponemos nunca el user_id directamente en la URL).
    """
    reset_link = f"{FRONTEND_URL}/reset-password?token={token}"

    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto; padding: 24px;">
      <div style="background-color:#242c3d; padding: 20px; border-radius: 16px 16px 0 0; text-align:center;">
        <h1 style="color:#ffffff; margin:0; font-size: 22px;">🎵 Jaye</h1>
      </div>
      <div style="background-color:#f8f9fc; padding: 28px; border-radius: 0 0 16px 16px;">
        <h2 style="color:#242c3d; font-size: 18px;">Recupera tu contraseña</h2>
        <p style="color:#475569; font-size: 14px; line-height: 1.6;">
          Hemos recibido una solicitud para restablecer la contraseña de tu cuenta en Jaye.
          Haz clic en el siguiente botón para crear una nueva contraseña:
        </p>
        <div style="text-align:center; margin: 28px 0;">
          <a href="{reset_link}"
             style="background-color:#8b5cf6; color:#ffffff; padding: 12px 28px;
                    border-radius: 12px; text-decoration:none; font-weight:bold; font-size: 14px;">
            Restablecer contraseña
          </a>
        </div>
        <p style="color:#94a3b8; font-size: 12px; line-height: 1.6;">
          Este enlace caduca en 15 minutos por seguridad. Si tú no solicitaste este cambio,
          puedes ignorar este correo: tu contraseña actual seguirá funcionando con normalidad.
        </p>
      </div>
    </div>
    """

    resend.Emails.send({
        "from": EMAIL_FROM,
        "to": [to_email],
        "subject": "Recupera tu contraseña en Jaye",
        "html": html_content,
    })