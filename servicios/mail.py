import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

from servicios.qr import imagen_qr

VARIABLES_NECESARIAS = ["SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS",
                        "MAIL_USUARIO_MOCK"]


class EnviadorSMTP:
    """Envía el mail real. Lee la configuración del archivo .env."""

    def __init__(self):
        load_dotenv()
        for variable in VARIABLES_NECESARIAS:
            if not os.getenv(variable):
                raise RuntimeError(f"Falta configurar {variable} en .env")
        self.host = os.getenv("SMTP_HOST")
        self.puerto = int(os.getenv("SMTP_PORT"))
        self.usuario = os.getenv("SMTP_USER")
        self.clave = os.getenv("SMTP_PASS")
        self.destino = os.getenv("MAIL_USUARIO_MOCK")

    def armar_mensaje(self, mail):
        mensaje = EmailMessage()
        mensaje["Subject"] = mail.asunto
        mensaje["From"] = self.usuario
        mensaje["To"] = self.destino
        mensaje.set_content(mail.cuerpo, charset="utf-8")
        numero = 1
        for texto in mail.qrs:
            mensaje.add_attachment(imagen_qr(texto), maintype="image",
                                   subtype="png",
                                   filename=f"qr_visitante_{numero}.png")
            numero += 1
        return mensaje

    def enviar(self, mail):
        mensaje = self.armar_mensaje(mail)
        with smtplib.SMTP(self.host, self.puerto, timeout=10) as servidor:
            servidor.starttls()
            servidor.login(self.usuario, self.clave)
            servidor.send_message(mensaje)
