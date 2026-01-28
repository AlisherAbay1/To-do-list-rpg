from redis.asyncio import Redis, ConnectionPool
from typing import Final

pool = ConnectionPool(host="localhost", port=6379, encoding="utf-8", decode_responses=True)
MAX_AGE: Final = 3600

async def get_redis_session():
    async with Redis(connection_pool=pool) as session:
        yield session
        