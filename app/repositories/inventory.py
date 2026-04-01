from sqlalchemy import select, delete
from app.models.inventory import Inventory
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Sequence
from uuid import UUID

class InventoryRepository:
    __slots__ = ("_session", )
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_items_in_inventory_by_user_id(self, user_id: str, offset: int, limit: int) -> Sequence[Inventory]:
        inventory = select(Inventory).where(Inventory.user_id == user_id).offset(offset).limit(limit)
        result = await self._session.scalars(inventory)
        return result.all()
    
    async def delete_item(self, item_id: UUID) -> None:
        item = delete(Inventory).where(Inventory.item_id == item_id)
        await self._session.execute(item)