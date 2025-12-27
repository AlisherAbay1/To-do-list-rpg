from app.models import User
from app.core import LocalSession
from sqlalchemy import select, exists, ColumnExpressionArgument
from fastapi import HTTPException

def does_exist_in_schema(*expression: ColumnExpressionArgument[bool]):
    with LocalSession.begin() as session:
        does_exist = session.execute(
            select(
                exists().where(*expression)
                )
            ).scalar()
    if does_exist:
        return True
    return False

def get_hashed_password_by_id(id):
    with LocalSession.begin() as session:
        password_hash = session.scalar(
            select(User.password).where(User.id == id)
            )
        
        if password_hash == None:
            raise HTTPException(404, "Hashed password not found")
        return password_hash
