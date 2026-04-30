from dataclasses import dataclass
from uuid import UUID
from src.app.application.dto.sentinel_types import Unset
from src.app.application.dto.tasks import TaskDetailDTO

@dataclass
class TaskCategoryDTO:
    id: UUID
    user_id: UUID
    title: str
    color: str

@dataclass
class CreateTaskCategoryDTO:
    title: str
    color: str

@dataclass
class UpdateTaskCategoryDTO:
    title: str | Unset
    color: str | Unset

@dataclass
class TaskCategoryWithTasksDTO:
    id: UUID
    user_id: UUID
    title: str
    color: str

    tasks: list[TaskDetailDTO]