from typing import Optional, Sequence
from uuid import UUID
from todo_rpg.domain import UserRank
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class UserRankRepository:
    __slots__ = ("_session",)

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_ranks_by_user_id(
        self, user_id: UUID, limit: int, offset: int
    ) -> Sequence[UserRank]:
        user_ranks = (
            select(UserRank)
            .where(UserRank.user_id == user_id)
            .limit(limit)
            .offset(offset)
        )
        result = await self._session.scalars(user_ranks)
        return result.all()

    async def get_rank_by_id(self, rank_id: UUID) -> Optional[UserRank]:
        user_rank = select(UserRank).where(UserRank.id == rank_id)
        result = await self._session.scalar(user_rank)
        return result
