from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    mysql_user: str = Field(
        default='streamserv',
        env='MYSQL_USER',
        alias='MYSQL_USER'
    )

    mysql_host: str = Field(
        default='localhost',
        env='MYSQL_HOST',
        alias='MYSQL_HOST'
    )

    mysql_password: str = Field(
        default='streamserv',
        env='MYSQL_PASSWORD',
        alias='MYSQL_PASSWORD'
    )

    mysql_database: str = Field(
        default='streamserv',
        env='MYSQL_DATABASE',
        alias='MYSQL_DATABASE'
    )

    ws_protocol: str = Field(
        default='ws',
        env='WS_PROTOCOL',
        alias='WS_PROTOCOL'
    )

    ws_host: str = Field(
        default='localhost',
        env='WS_HOST',
        alias='WS_HOST'
    )

    ws_port: str = Field(
        default='5000',
        env='WS_PORT',
        alias='WS_PORT'
    )

    class Config:
        env_file = ".env"


def load_config():
    return Config()
