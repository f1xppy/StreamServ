import redis
from .config import get_broker_config


async def connect_redis() -> redis.Redis:
    brokerConfig = get_broker_config()
    return redis.Redis(host='localhost', port=6379, decode_responses=True)
