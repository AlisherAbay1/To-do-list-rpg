from dataclasses import dataclass
from uuid import UUID

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