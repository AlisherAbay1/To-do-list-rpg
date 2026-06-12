from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from todo_rpg.domain import Item, Task, ItemRequirement


class ItemRepository:
    __slots__ = ("_session",)

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_items(self, limit: int, offset: int) -> Sequence[Item]:
        items = select(Item).limit(limit).offset(offset)
        result = await self._session.scalars(items)
        return result.all()

    async def get_items_by_user_id(
        self, user_id: UUID, limit: int, offset: int, get_deleted: bool
    ) -> Sequence[Item]:
        items = select(Item).where(Item.user_id == user_id).limit(limit).offset(offset)
        if not get_deleted:
            items = items.where(Item.deleted == False)
        result = await self._session.scalars(items)
        return result.all()

    async def get_item_by_id(self, item_id: UUID) -> Optional[Item]:
        item = select(Item).where(Item.id == item_id).with_for_update()
        result = await self._session.scalar(item)
        return result

    async def get_items_by_task_id(self, task_id: UUID) -> Sequence[Item]:
        items = select(Item).join(Task.items).where(Task.id == task_id)
        result = await self._session.scalars(items)
        return result.all()

    async def get_item_by_id_with_requirements_contains_skill(
        self, item_id: UUID, user_id: UUID
    ) -> Optional[Item]:
        item = (
            select(Item)
            .where(Item.id == item_id, Item.user_id == user_id)
            .options(selectinload(Item.requirements).joinedload(ItemRequirement.skill))
            .with_for_update()
        )
        result = await self._session.scalar(item)
        return result

    async def delete_requirement(self, item_id: UUID, skill_id: UUID) -> None:
        stmt = delete(ItemRequirement).where(
            ItemRequirement.item_id == item_id, ItemRequirement.skill_id == skill_id
        )
        await self._session.execute(stmt)

    async def delete(self, item_id: UUID):
        item = delete(Item).where(Item.id == item_id)
        await self._session.execute(item)
