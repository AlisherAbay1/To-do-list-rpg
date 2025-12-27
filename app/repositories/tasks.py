from app.models.tasks import Task
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_local_session
from app.repositories.base import BaseCRUD

class TaskCRUD(BaseCRUD[Task]):
    def __init__(self, session: Session = Depends(get_local_session)):
        super().__init__(model=Task, session=session)

    def select_by_id(self):
        return self.select(self._model.id == id)