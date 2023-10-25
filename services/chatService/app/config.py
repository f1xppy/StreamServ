from pydantic_settings import BaseSettings
from os import getenv


class BrokerConfig(BaseSettings):
    host: str = getenv("CHAT_BROKER_HOST","0.0.0.0")
    port: int = getenv("CHAT_BROKER_PORT", 6000)
    db: int = getenv("CHAT_BROKER_DB", 2)
    channel_name: str = getenv("CHAT_CHANNEL_NAME", "chat_channel")


def get_broker_config():
    return BrokerConfig()
