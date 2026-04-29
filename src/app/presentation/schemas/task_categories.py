from pydantic import BaseModel
from uuid import UUID

class TaskCategoriesSchema(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    color: str