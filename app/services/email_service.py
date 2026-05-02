import smtplib
import os
from email.mime.text import MIMEText

import os
from dotenv import load_dotenv

load_dotenv()  # Esta línea busca el archivo .env y carga los datos

# Ahora ya puedes usarlas:
email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")
def send_email(to_email: str, code: str):
    try:
        # Credenciales (Asegúrate de usar 'Contraseña de Aplicación' de Google)
        sender = os.getenv("EMAIL_USER")
        password = os.getenv("EMAIL_PASS")

        if not sender or not password:
            print("Error: No se encontraron las variables de entorno de email.")
            return

        # Diseño del correo
        cuerpo = f"""
        <h2>Verificación de Cuenta</h2>
        <p>Tu código de seguridad es: <b>{code}</b></p>
        <p>Este código expirará en 5 minutos.</p>
        """
        
        msg = MIMEText(cuerpo, "html")
        msg["Subject"] = "Código de Verificación - Registro Estudiantes"
        msg["From"] = sender
        msg["To"] = to_email

        # Configuración SMTP
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()

        print(f"Correo enviado exitosamente a {to_email}")

    except Exception as e:
        print(f"Error crítico enviando correo: {str(e)}")