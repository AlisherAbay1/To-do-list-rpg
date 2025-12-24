from abc import ABC
from typing import ClassVar, Type
from app.models.base import Base
from app.core.database import get_local_session
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from fastapi import Depends

class BaseCRUD(ABC):
    model: ClassVar[Type[Base]]

    def __init__(self, session: Session = Depends(get_local_session)):
        self._session = session

    def _get(self, field, value):
        value = select(self.model).where(field == value)
        return self._session.scalar(value)
    
    def _get_list(self, field, value):
        values = select(self.model).where(field == value)
        return self._session.scalars(values)
    
    def _create(self, commit: bool = True, **data: dict):
        obj = self.model(**data)
        self._session.add(obj)
        if commit:
            self._session.commit()
            self._session.refresh(obj)
        return obj

    def _delete(self, field, value):
        del_stmt = delete(self.model).where(field == value).returning(self.model)
        result = self._session.execute(del_stmt)
        self._session.commit()
        if result.scalar():
            return True
        return False
    
    def _update(self, field, value, commit: bool = True, **data):
        upd_stmt = update(self.model).where(field == value).values(**data).returning(self.model)
        obj = self._session.scalar(upd_stmt)
        if commit:
            self._session.commit()
            self._session.refresh(obj)
        return obj