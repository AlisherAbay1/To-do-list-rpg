from app.repositories.base import BaseCRUD
from app.models.users import User
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_local_session
from app.core.database import LocalSession

class UserCRUD(BaseCRUD[User]):
    def __init__(self, session: Session = Depends(get_local_session)):
        super().__init__(model=User, session=session)

def get_password_hash_by_username(username):
    with LocalSession.begin() as session:
        password_hash = session.scalar(
            select(User.password).where(User.username == username)
            )
        
        if password_hash == None:
            raise HTTPException(400, "pass")
        return password_hash