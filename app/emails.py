from fastapi_mail import MessageSchema, MessageType, FastMail
from starlette.responses import JSONResponse

from app.schemas import EmailSchema

from fastapi_mail import ConnectionConfig

import secrets

conf = ConnectionConfig(
    MAIL_USERNAME="shainurov.mar@yandex.ru",
    MAIL_PASSWORD="mtrqvcttesattpwj",
    MAIL_FROM="shainurov.mar@yandex.ru",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.yandex.ru",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

html = """
<p>
Hello, dear friend! 
Here is your verification code {0}. 
Please, use it to verify you email. 
Thanks!
</p> 
"""


async def send_mail(email: EmailSchema, verification_code):
    message = MessageSchema(
        subject="Email verification",
        recipients=email.model_dump().get("email"),
        body=html.format(verification_code),
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)


def get_verification_code() -> str:
    code = secrets.token_hex(6)
    return code
