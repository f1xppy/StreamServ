from pydantic import Field, MySQLDsn, SecretStr, FilePath
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    mysql_dsn: MySQLDsn = Field(
        default='mysql+asyncmy://streamserv:streamserv@localhost/streamserv',
        env='MYSQL_DSN',
        alias='MYSQL_DSN'
    )

    mail_username: str = Field(
        default='streamserv@inbox.ru',
        env='MAIL_USERNAME',
        alias='MAIL_USERNAME'
    )
    mail_password: str = Field(
        default='brBLU4Wmffrb8M2nrUXv',
        env='MAIL_PASSWORD',
        alias='MAIL_PASSWORD'
    )
    mail_port: str = Field(
        default=465,
        env='MAIL_PORT',
        alias='MAIL_PORT'
    )
    mail_server: str = Field(
        default='streamserv@inbox.ru',
        env='MAIL_SERVER',
        alias='MAIL_SERVER'
    )

    jwt_secret: SecretStr = Field(
        default='jwt_secret',
        env='JWT_SECRET',
        alias='JWT_SECRET'
    )

    reset_password_token_secret: SecretStr = Field(
        default='reset_password_token_secret',
        env='RESET_PASSWORD_TOKEN_SECRET',
        alias='RESET_PASSWORD_TOKEN_SECRET'
    )

    verification_token_secret: SecretStr = Field(
        default='verification_token_secret',
        env='VERIFICATION_TOKEN_SECRET',
        alias='VERIFICATION_TOKEN_SECRET'
    )

    default_groups_config_path: FilePath = Field(
        default='default-groups.json',
        env='DEFAULT_GROUPS_CONFIG_PATH',
        alias='DEFAULT_GROUPS_CONFIG_PATH'
    )

    class Config:
        env_file = ".env"


def load_config():
    app_config: Config = Config()
    return app_config
