from uuid import uuid4
from secrets import token_urlsafe
from redis.asyncio import Redis
from app.core.redis_config import MAX_AGE
from typing import Optional

class RedisRepository:
    __slots__ = ("_session",)
    def __init__(self, session: Redis):
        self._session = session

    async def create_session(self, user_id: str) -> str:
        session_token = token_urlsafe(32)
        await self._session.setex(f"session:{session_token}", MAX_AGE, user_id)
        return session_token

    async def extend_token_time(self, session_token: str) -> None:
        self._session.expire(session_token, MAX_AGE)

    async def delete_session(self, session_token: str) -> None:
        await self._session.delete(f"session:{session_token}")

    async def get_user_id_by_session_token(self, session_token: str) -> Optional[str]:
        id = await self._session.get(f"session:{session_token}")
        if id == "None":
            id = None
        return id

    async def get_session_time(self, session_token: str) -> int: 
        return await self._session.ttl(f"session:{session_token}")
    