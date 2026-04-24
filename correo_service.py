import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.office365.com",
    MAIL_FROM_NAME="Sistema Eventos CUL",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def enviar_correo(destinatario: EmailStr, asunto: str, mensaje: str):
    message = MessageSchema(
        subject=asunto,
        recipients=[destinatario],
        body=mensaje,
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)