from app.models import User
from app.core import LocalSession
from sqlalchemy import select, exists, ColumnExpressionArgument
from fastapi import HTTPException

async def does_exist_in_schema(*expression: ColumnExpressionArgument[bool]):
    async with LocalSession.begin() as session:
        does_exist = await session.execute(
            select(
                exists().where(*expression)
                )
            )
    if does_exist.scalar():
        return True
    return False

async def get_hashed_password_by_id(id):
    async with LocalSession.begin() as session:
        password_hash = await session.scalar(
            select(User.password).where(User.id == id)
            )
        
        if password_hash == None:
            raise HTTPException(404, "Hashed password not found")
        return password_hash
