from src.app.infrastructure.database.models.items import Item
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Optional, Sequence
from uuid import UUID

class ItemRepository:
    __slots__ = ("_session",)
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_items(self, limit: int, offset: int) -> Sequence[Item]:
        skills = select(Item).limit(limit).offset(offset)
        result = await self._session.scalars(skills)
        return result.all()
    
    async def get_items_by_user_id(self, user_id: UUID, limit: int, offset: int) -> Sequence[Item]:
        skills = select(Item).where(Item.user_id == user_id).limit(limit).offset(offset)
        result = await self._session.scalars(skills)
        return result.all()
    
    async def get_item_by_id(self, item_id: UUID) -> Optional[Item]:
        item = select(Item).where(Item.id == item_id)
        result = await self._session.scalar(item)
        return result

    async def delete(self, item_id: UUID):
        item = delete(Item).where(Item.id == item_id)
        await self._session.execute(item)