from typing import Sequence, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from todo_rpg.domain import Inventory


class InventoryRepository:
    __slots__ = ("_session",)

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_inventory_items_by_user_id(
        self, user_id: UUID, limit: int, offset: int
    ) -> Sequence[Inventory]:
        inventory_items = (
            select(Inventory)
            .where(Inventory.user_id == user_id)
            .offset(offset)
            .limit(limit)
        )
        result = await self._session.scalars(inventory_items)
        return result.all()

    async def get_inventory_item_by_id(
        self, inventory_item_id: UUID
    ) -> Optional[Inventory]:
        inventory_item = (
            select(Inventory).where(Inventory.id == inventory_item_id).with_for_update()
        )
        result = await self._session.scalar(inventory_item)
        return result

    async def get_inventory_item_by_item_id(
        self, item_id: UUID, user_id: UUID
    ) -> Optional[Inventory]:
        inventory_item = (
            select(Inventory)
            .where(Inventory.item_id == item_id, Inventory.user_id == user_id)
            .with_for_update()
        )
        result = await self._session.scalar(inventory_item)
        return result

    async def delete(self, inventory_item: Inventory) -> None:
        await self._session.delete(inventory_item)
