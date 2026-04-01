from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import Base

class TransactionAlchemyManager:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None: 
        await self._session.commit()

    async def flush(self) -> None: 
        await self._session.flush()

    async def save(self, model: Base) -> None:
        self._session.add(model)

    async def delete(self, model: Base) -> None:
        await self._session.delete(model)