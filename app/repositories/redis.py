from uuid import uuid4, UUID
from redis.asyncio import Redis
from app.core.redis_config import MAX_AGE
from typing import Optional

class RedisRepository:
    __slots__ = ("_session",)
    def __init__(self, session: Redis):
        self._session = session

    async def create_session(self, user_id: str) -> str:
        session_id = str(uuid4())
        await self._session.setex(f"session:{session_id}", MAX_AGE, user_id)
        return session_id
    
    async def delete_session(self, session_id: str) -> None:
        is_deleted = await self._session.delete(f"session:{session_id}")
    
    async def get_user_id_by_session_id(self, session_id: str) -> Optional[str]:
        id = await self._session.get(f"session:{session_id}")
        if id == "None":
            id = None
        return id