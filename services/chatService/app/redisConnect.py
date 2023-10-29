import redis


async def connect_redis() -> redis.Redis:
    return redis.Redis(host='localhost', port=6379, decode_responses=True)
