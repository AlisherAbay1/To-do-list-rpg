from dotenv import dotenv_values
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

database_url = f"postgresql+asyncpg://postgres:{dotenv_values(r".env")["DB_PASSWORD"]}@localhost:5432/to-do-list-rpg"
engine = create_async_engine(database_url)

LocalSession = async_sessionmaker(bind=engine)

async def get_local_session():
    async with LocalSession() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e