from app.repositories.base import BaseCRUD
from app.models.users import User
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_local_session

class UserCRUD(BaseCRUD[User]):
    def __init__(self, session: AsyncSession = Depends(get_local_session)):
        super().__init__(model=User, session=session)

