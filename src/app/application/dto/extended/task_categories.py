from dataclasses import dataclass
from uuid import UUID
from src.app.application.dto import TaskDetailDTO


@dataclass
class TaskCategoryWithTasksDTO:
    id: UUID
    user_id: UUID
    title: str
    color: str

    tasks: list[TaskDetailDTO]
