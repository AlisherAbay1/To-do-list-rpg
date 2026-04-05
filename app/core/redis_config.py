from redis.asyncio import Redis, ConnectionPool
from typing import Final

MAX_AGE: Final = 3600

def redis_client() -> Redis:
    pool = ConnectionPool(host="localhost", port=6379, encoding="utf-8", decode_responses=True)
    return Redis(connection_pool=pool)