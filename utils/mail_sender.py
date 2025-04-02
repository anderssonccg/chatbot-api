import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_SERVER = os.getenv("MAIL_SERVER")
DOMAIN = os.getenv("DOMAIN")

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)


async def send_verification_email(email: str, token: str):
    token = token["access_token"]
    verification_url = f"{DOMAIN}/users/verify-email?token={token}"
    message = MessageSchema(
        subject="Verifica tu correo",
        recipients=[email],
        body=f"Confirma tu cuenta haciendo clic en este enlace: {verification_url}",
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message)
