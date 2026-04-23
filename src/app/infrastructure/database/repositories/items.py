from src.app.infrastructure.database.models import Item, Task
from src.app.infrastructure.mappers import ItemMapper
from src.app.domain import ItemDomain
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Optional, Sequence
from uuid import UUID

class ItemRepository:
    __slots__ = ("_session",)
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_items(self, limit: int, offset: int) -> Sequence[Item]:
        items = select(Item).limit(limit).offset(offset)
        result = await self._session.scalars(items)
        return result.all()
    
    async def get_items_by_user_id(self, user_id: UUID, limit: int, offset: int) -> Sequence[Item]:
        items = select(Item).where(Item.user_id == user_id).limit(limit).offset(offset)
        result = await self._session.scalars(items)
        return result.all()
    
    async def get_item_by_id(self, item_id: UUID) -> Optional[Item]:
        item = select(Item).where(Item.id == item_id)
        result = await self._session.scalar(item)
        return result
    
    async def get_items_by_task_id(self, task_id: UUID) -> list[ItemDomain]:
        items = select(Item).join(Task.items).where(Task.id == task_id)
        result = await self._session.scalars(items)
        return ItemMapper.to_domain_list(result.all())

    async def delete(self, item_id: UUID):
        item = delete(Item).where(Item.id == item_id)
        await self._session.execute(item)