from typing import Sequence, Optional
from uuid import UUID
from todo_rpg.domain import ShopTransaction
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from todo_rpg.application.dto import ShopTransactionFiltersDTO


class ShopTransactionRepository:
    __slots__ = ("_session",)

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_shop_transactions_by_user_id(
        self, user_id: UUID, limit: int, offset: int, filters: ShopTransactionFiltersDTO
    ) -> Sequence[ShopTransaction]:
        stmt = (
            select(ShopTransaction)
            .where(ShopTransaction.user_id == user_id)
            .limit(limit)
            .offset(offset)
        )

        if filters.date_from:
            stmt = stmt.where(ShopTransaction.date >= filters.date_from)
        if filters.date_to:
            stmt = stmt.where(ShopTransaction.date <= filters.date_to)
        if filters.sum_from:
            stmt = stmt.where(ShopTransaction.price >= filters.sum_from)
        if filters.sum_to:
            stmt = stmt.where(ShopTransaction.price <= filters.sum_to)

        shop_transactions = await self._session.scalars(stmt)
        return shop_transactions.all()

    async def get_shop_transaction_by_id(
        self, shop_transaction_id: UUID
    ) -> Optional[ShopTransaction]:
        stmt = select(ShopTransaction).where(ShopTransaction.id == shop_transaction_id)
        shop_transaction = await self._session.scalar(stmt)
        return shop_transaction
