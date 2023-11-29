import uuid
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin
from app.users import secretprovider
from app import config
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from jinja2 import Template
from app.users import models

app_config: config.Config = config.load_config()

conf = ConnectionConfig(
    MAIL_USERNAME=app_config.mail_username,
    MAIL_PASSWORD=app_config.mail_password,
    MAIL_PORT=app_config.mail_port,
    MAIL_SERVER=app_config.mail_server,
    MAIL_FROM="streamserv@inbox.ru",
    MAIL_FROM_NAME="StreamServ",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True
)

fm = FastMail(conf)


class UserManager(UUIDIDMixin, BaseUserManager[models.User, uuid.UUID]):

    async def on_after_register(self, user: models.User, request: Optional[Request] = None):
        html_file = open('app/users/html_templates/register_mail.html', 'r')
        html_content = html_file.read()
        html_file.close()
        template = Template(html_content)

        message = MessageSchema(
            subject="You created account",
            recipients=[user.email],
            body=template.render(name=user.real_name),
            subtype=MessageType.html)

        await fm.send_message(message)

        '''async for session in aiter(models.get_async_session()):
            try:
                g = geocoder.ipinfo('me')
                geopos = g.latlng
                logging.info(f"POINT ({geopos[0]} {geopos[1]})")
                user.geopos = f"POINT ({geopos[0]} {geopos[1]})"
                logging.info(user.geopos)
            finally:
                await session.commit()'''


    async def on_after_forgot_password(
            self, user: models.User, token: str, request: Optional[Request] = None
    ):
        html_file = open('app/users/html_templates/reset_password_mail.html', 'r')
        html_content = html_file.read()
        html_file.close()
        template = Template(html_content)

        message = MessageSchema(
            subject="Reset password",
            recipients=[user.email],
            body=template.render(name=user.real_name, token=token),
            subtype=MessageType.html)

        await fm.send_message(message)

    async def on_after_request_verify(
            self, user: models.User, token: str, request: Optional[Request] = None
    ):
        html_file = open('app/users/html_templates/verification_mail.html', 'r')
        html_content = html_file.read()
        html_file.close()
        template = Template(html_content)

        message = MessageSchema(
            subject="Verify",
            recipients=[user.email],
            body=template.render(name=user.real_name, token=token),
            subtype=MessageType.html)

        await fm.send_message(message)



async def get_user_manager(
        user_db=Depends(models.get_user_db),
        secret_provider: secretprovider.SecretProvider = Depends(secretprovider.get_secret_provider)
):
    user_manager = UserManager(user_db)
    user_manager.reset_password_token_secret = secret_provider.reset_password_token_secret
    user_manager.verification_token_secret = secret_provider.verification_token_secret
    yield user_manager
