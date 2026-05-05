import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Cargar variables del .env
load_dotenv()

# Variables de entorno
API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = os.getenv("FROM_EMAIL")

def send_email(to_email: str, code: str):
    """
    Envía un correo con código OTP usando SendGrid
    """

    if not API_KEY or not FROM_EMAIL:
        print("Error: Faltan variables de entorno (SENDGRID_API_KEY o FROM_EMAIL)")
        return

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject="Código de Verificación",
        html_content=f"""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #333;">Verificación de Cuenta</h2>
            <p>Tu código de seguridad es:</p>
            <h1 style="color: #007BFF;">{code}</h1>
            <p>Este código expirará en 5 minutos.</p>
            <hr>
            <small>Si no solicitaste este código, ignora este mensaje.</small>
        </div>
        """
    )

    try:
        sg = SendGridAPIClient(API_KEY)
        response = sg.send(message)

        print("Correo enviado correctamente")
        print("Status Code:", response.status_code)

    except Exception as e:
        print("Error enviando correo:", str(e))