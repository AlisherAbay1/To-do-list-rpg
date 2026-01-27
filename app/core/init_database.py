from app.models.base import Base
from app.core.database import engine
from sqlalchemy import text
import pathlib
import asyncio

async def create_database_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database created succesfully")

async def create_extensions_and_functions():
    async with engine.begin() as connection:
        await connection.execute(text('CREATE EXTENSION IF NOT EXISTS pgcrypto;'))
        await connection.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
    
    path = pathlib.Path(__file__).parent / "sql" / "functions" / "uuid_generate_v7.sql"

    with open(path, "r") as uuidv7_generator:
        async with engine.begin() as connection:
            await connection.execute(text(uuidv7_generator.read()))
    print("Extensions and functions were succesfully created")

async def main():
    await create_extensions_and_functions()
    await create_database_models()

if __name__ == '__main__':
    asyncio.run(main())
    