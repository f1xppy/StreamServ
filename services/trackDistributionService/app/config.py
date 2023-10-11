from pydantic import MongoDsn, Field
from pydantic_settings import BaseSettings
import pydantic_core


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

    class Config:
        env_file = ".env"


def load_config():
    return Config()


'''from dotenv import load_dotenv
import os

load_dotenv()
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")'''
