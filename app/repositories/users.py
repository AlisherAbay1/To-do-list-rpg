from app.models.users import User
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Sequence
from uuid import UUID

class UserRepository:
    __slots__ = ("_session")
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all_users(self, limit: int, offset: int) -> Sequence[User]:
        stmt = select(User).limit(limit).offset(offset)
        users = await self._session.scalars(stmt)
        return users.all()
    
    async def get_user(self, user_id: UUID) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        user = await self._session.scalar(stmt)
        return user
    
    async def get_user_by_username(self, username: str) -> Optional[User]:
        stmt = select(User).where(User.username == username)
        user = await self._session.scalar(stmt)
        return user
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        user = await self._session.scalar(stmt)
        return user
    
    def save(self, user: User) -> None:
        self._session.add(user)

    async def delete(self, user: User) -> None:
        await self._session.delete(user)

    async def does_username_exists(self, username: str) -> Optional[bool]:
        does_exist = await self._session.scalar(
            select(
                exists().where(User.username == username)
                )
            )
        return does_exist
    
    async def does_email_exists(self, email: str) -> Optional[bool]:
        does_exist = await self._session.scalar(
            select(
                exists().where(User.email == email)
                )
            )
        return does_exist