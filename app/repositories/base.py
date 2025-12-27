from abc import ABC
from typing import TypeVar, Generic
from app.models.base import Base
from sqlalchemy import select, delete, update, ColumnExpressionArgument, insert
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Base)

class BaseCRUD(ABC, Generic[ModelType]):
    __slots__ = ("_session", "_model")
    def __init__(self, model: type[ModelType], session: Session):
        self._session = session
        self._model = model

    def select(self, *expression: ColumnExpressionArgument[bool]):
        value = select(self._model).where(*expression)
        return self._session.scalar(value) or self._model()
    
    def select_many(self, limit=None, offset=None, *expression: ColumnExpressionArgument[bool]):
        values = select(self._model).where(*expression).limit(limit).offset(offset)
        return self._session.scalars(values)
    
    def insert(self, **data: dict):
        insert_stmt = insert(self._model).values(**data).returning(self._model)
        inserted = self._session.scalar(insert_stmt)
        self._session.commit()
        return inserted

    def insert_many(self, data_list: list[dict]):
        insert_stmt = insert(self._model).values(data_list).returning(self._model)
        inserted = self._session.scalars(insert_stmt).all()
        self._session.commit()
        return inserted
    
    def delete(self, *expression: ColumnExpressionArgument[bool]):
        del_stmt = delete(self._model).where(*expression).returning(self._model)
        result = self._session.scalar(del_stmt)
        self._session.commit()
        return result

    def update(self, *expression: ColumnExpressionArgument[bool], **data):
        upd_stmt = update(self._model).where(*expression).values(**data).returning(self._model)
        obj = self._session.scalar(upd_stmt)
        self._session.commit()
        return obj