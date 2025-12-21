from app.models.base import Base
from app.core.database import engine
from sqlalchemy import text
import pathlib

def create_database_models():
    Base.metadata.create_all(bind=engine)
    print("Database created succesfully")

def create_extensions_and_functions():
    with engine.begin() as connection:
        connection.execute(text('CREATE EXTENSION IF NOT EXISTS pgcrypto;'))
        connection.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
    
    path = pathlib.Path(__file__).parent / "sql" / "functions" / "uuid_generate_v7.sql"

    with open(path, "r") as uuidv7_generator:
        with engine.begin() as connection:
            connection.execute(text(uuidv7_generator.read()))
    print("Extensions and functions were succesfully created")

if __name__ == '__main__':
    create_extensions_and_functions()
    create_database_models()