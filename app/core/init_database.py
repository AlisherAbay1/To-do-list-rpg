from app.models.base import Base
from app.core.database import engine
from sqlalchemy import text
import pathlib
import asyncio

async def create_database_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database created succesfully")

if __name__ == '__main__':
    asyncio.run(create_database_models())
    