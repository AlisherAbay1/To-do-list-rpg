from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

engine = create_engine(f"postgresql+psycopg2://postgres:{dotenv_values(r"app\.env")["DB_PASSWORD"]}@localhost:5432/to-do-list-rpg")

LocalSession = sessionmaker(bind=engine)

def get_local_session():
    with LocalSession() as session:
        yield session