from pydantic import BaseModel
from uuid import UUID
from src.app.presentation.schemas import TaskSchemaRead

class TaskCategoryWithTasksSchema(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    color: str

    tasks: list[TaskSchemaRead]