from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
    AsyncEngine,
)
from sqlalchemy.engine import URL
from redis.asyncio import Redis, ConnectionPool
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.transaction_interfaces import TransactionProtocol
from todo_rpg.infrastructure.database.repositories import (
    RedisRepository,
    TransactionAlchemyManager,
)
from collections.abc import AsyncGenerator
from todo_rpg.infrastructure.config import config


class AppProvider(Provider):
    @provide(scope=Scope.APP)
    def get_db_url(self) -> URL:
        return config.database.db_url

    @provide(scope=Scope.APP)
    async def get_async_engine(self, url: URL) -> AsyncGenerator[AsyncEngine, None]:
        engine = create_async_engine(url)
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def get_session_maker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine)

    @provide(scope=Scope.REQUEST)
    async def get_pgsql_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_redis_connection_pool(self) -> ConnectionPool:
        pool = ConnectionPool(
            host=config.redis.host,
            port=config.redis.port,
            encoding=config.redis.encoding,
            decode_responses=True,
        )
        return pool

    @provide(scope=Scope.APP)
    async def get_redis_session(self, pool: ConnectionPool) -> AsyncGenerator[Redis]:
        redis = Redis.from_pool(pool)
        yield redis
        await redis.aclose()

    redis_session = provide(
        RedisRepository, scope=Scope.REQUEST, provides=RedisRepositoryProtocol
    )
    transaction = provide(
        TransactionAlchemyManager, scope=Scope.REQUEST, provides=TransactionProtocol
    )
