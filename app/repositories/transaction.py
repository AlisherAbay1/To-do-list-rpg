from sqlalchemy.ext.asyncio import AsyncSession

class TransactionAlchemyManager:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self): 
        await self._session.commit()

    async def flush(self): 
        await self._session.flush()