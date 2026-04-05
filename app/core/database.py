from dotenv import dotenv_values
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

def get_new_session_maker() -> async_sessionmaker[AsyncSession]:
    database_url = f"postgresql+asyncpg://postgres:{dotenv_values(r".env")["DB_PASSWORD"]}@localhost:5432/to-do-list-rpg"
    engine = create_async_engine(database_url)
    
    return async_sessionmaker(bind=engine)