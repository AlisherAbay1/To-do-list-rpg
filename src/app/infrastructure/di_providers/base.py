from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from redis.asyncio import Redis
from src.app.core.database import get_new_session_maker
from src.app.core.redis_config import redis_client
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.infrastructure.database.repositories import RedisRepository, TransactionAlchemyManager
from collections.abc import AsyncGenerator

class AppProvider(Provider):
    @provide(scope=Scope.APP)
    def get_session_maker(self) -> async_sessionmaker[AsyncSession]:
        return get_new_session_maker()

    @provide(scope=Scope.REQUEST)
    async def get_pgsql_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession]:
        async with session_maker() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise e

    @provide(scope=Scope.REQUEST)
    async def get_redis_session(self) -> AsyncGenerator[Redis]:
        async with redis_client() as session:
            yield session

    redis_session = provide(RedisRepository, scope=Scope.REQUEST, provides=RedisRepositoryProtocol)
    transaction = provide(TransactionAlchemyManager, scope=Scope.REQUEST, provides=TransactionProtocol)