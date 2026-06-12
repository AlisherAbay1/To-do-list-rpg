from pydantic import BaseModel
from uuid import UUID


class UserRankSchemaRead(BaseModel):
    id: UUID
    user_id: UUID
    title: str


class UserRankSchemaCreate(BaseModel):
    title: str


class UserRankSchemaUpdate(BaseModel):
    title: str | None
