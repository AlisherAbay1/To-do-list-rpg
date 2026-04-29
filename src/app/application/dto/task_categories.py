from dataclasses import dataclass
from uuid import UUID

@dataclass
class TaskCategoriesDTO:
    id: UUID
    user_id: UUID
    title: str
    color: str