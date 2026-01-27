from app.models.items import Item
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Sequence

class ItemRepository:
    __slots__ = ("_session")
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_items(self, limit: int, offset: int) -> Sequence[Item]:
        skills = select(Item).limit(limit).offset(offset)
        result = await self._session.scalars(skills)
        return result.all()
    
    async def get_items_by_user_id(self, user_id, limit: int, offset: int) -> Sequence[Item]:
        skills = select(Item).where(Item.user_id == user_id).limit(limit).offset(offset)
        result = await self._session.scalars(skills)
        return result.all()
    
    async def get_item_by_id(self, item_id) -> Optional[Item]:
        item = select(Item).where(Item.id == item_id)
        result = await self._session.scalar(item)
        return result
    
    def save(self, item: Item):
        self._session.add(item)

    async def delete(self, item: Item):
        await self._session.delete(item)