from app.models.skills import Skill
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.database import get_local_session
from app.repositories.base import BaseCRUD

class SkillCRUD(BaseCRUD[Skill]):
    def __init__(self, session: AsyncSession = Depends(get_local_session)):
        super().__init__(model=Skill, session=session)

    def select_by_id(self):
        return self.select(self._model.id == id)