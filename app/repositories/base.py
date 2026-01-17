from abc import ABC
from typing import TypeVar, Generic, Optional, Sequence
from app.models.base import Base
from sqlalchemy import select, delete, update, ColumnExpressionArgument, insert, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=Base)

class BaseCRUD(ABC, Generic[ModelType]):
    __slots__ = ("_session", "_model")
    def __init__(self, model: type[ModelType], session: AsyncSession):
        self._session = session
        self._model = model

    async def select(self, *expression: ColumnExpressionArgument[bool]) -> Optional[ModelType]:
        value = select(self._model).where(*expression)
        return await self._session.scalar(value)
    
    async def select_many(self, limit=None, offset=None, *expression: ColumnExpressionArgument[bool]) -> ScalarResult[ModelType]:
        values = select(self._model).where(*expression).limit(limit).offset(offset)
        return await self._session.scalars(values)

    async def insert(self, **data: dict) -> Optional[ModelType]:
        insert_stmt = insert(self._model).values(**data).returning(self._model)
        inserted = await self._session.scalar(insert_stmt)
        await self._session.commit()
        return inserted

    async def insert_many(self, data_list: list[dict]) -> Sequence[ModelType]:
        insert_stmt = insert(self._model).values(data_list).returning(self._model)
        inserted = (await self._session.scalars(insert_stmt)).all()
        await self._session.commit()
        return inserted
    
    async def delete(self, *expression: ColumnExpressionArgument[bool]) -> Optional[ModelType]:
        del_stmt = delete(self._model).where(*expression).returning(self._model)
        result = await self._session.scalar(del_stmt)
        await self._session.commit()
        return result

    async def update(self, *expression: ColumnExpressionArgument[bool], **data) -> Optional[ModelType]:
        upd_stmt = update(self._model).where(*expression).values(**data).returning(self._model)
        obj = await self._session.scalar(upd_stmt)
        await self._session.commit()
        return obj
    
    async def update_flush(self, *expression: ColumnExpressionArgument[bool], **data) -> Optional[ModelType]:
        upd_stmt = update(self._model).where(*expression).values(**data).returning(self._model)
        obj = await self._session.scalar(upd_stmt)
        await self._session.flush()
        return obj