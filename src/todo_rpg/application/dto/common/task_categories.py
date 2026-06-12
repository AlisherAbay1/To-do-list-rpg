from dataclasses import dataclass
from uuid import UUID
from todo_rpg.application.dto.sentinel_types import Unset


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
