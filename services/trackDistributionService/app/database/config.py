from pydantic import MongoDsn, Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    mongo_dsn: MongoDsn = Field(
        default='mongodb://user:pass@localhost:27017',
        env='MONGO_DSN',
        alias='MONGO_DSN'
    )
    int_example: int = Field(
        default=6,
        env='INT_EXAMPLE',
        alias='INT_EXAMPLE'
    )
    bool_example: bool = Field(
        default=False,
        env='BOOL_EXAMPLE',
        alias='BOOL_EXAMPLE'
    )
    minio_access_key: str = Field(
        default=' ',
        env='MINIO_ACCESS_KEY',
        alias='MINIO_ACCESS_KEY'
    )
    minio_secret_key: str = Field(
        default=' ',
        env='MINIO_SECRET_KEY',
        alias='MINIO_SECRET_KEY'
    )
    minio_root_user: str = Field(
        default=' ',
        env='MINIO_ROOT_USER',
        alias='MINIO_ROOT_USER'
    )
    minio_root_password: str = Field(
        default=' ',
        env='MINIO_ROOT_PASSWORD',
        alias='MINIO_ROOT_PASSWORD'
    )



    class Config:
        env_file = ".env"


def load_config():
    return Config()

