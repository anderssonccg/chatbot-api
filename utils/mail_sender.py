import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Environment, FileSystemLoader

from dotenv import load_dotenv

load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_SERVER = os.getenv("MAIL_SERVER")
DOMAIN = os.getenv("DOMAIN")

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_USERNAME,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)


async def send_verification_email(email: str, token: str):
    token = token["access_token"]
    verification_url = f"{DOMAIN}/users/verify-email?token={token}"

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("email_verification.html")
    html_content = template.render(verification_url=verification_url)

    message = MessageSchema(
        subject="Verifica tu correo",
        recipients=[email],
        body=html_content,
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message)


async def send_reset_password_email(email: str, token: str):
    token = token["access_token"]
    verification_url = f"{DOMAIN}/users/reset-password-confirm?token={token}"
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("reset_password.html")
    html_content = template.render(verification_url=verification_url)

    message = MessageSchema(
        subject="Recuperar contraseña",
        recipients=[email],
        body=html_content,
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message)
