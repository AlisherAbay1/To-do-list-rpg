from pydantic import BaseModel
from uuid import UUID
from src.app.presentation.schemas.tasks import TaskSchemaRead

class TaskCategoriesSchema(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    color: str

class CreateTaskCategorySchema(BaseModel):
    title: str
    color: str

class UpdateTaskCategorySchema(BaseModel):
    title: str | None = None
    color: str | None = None

class TaskCategoryWithTasksDTO(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    color: str

    tasks: list[TaskSchemaRead]