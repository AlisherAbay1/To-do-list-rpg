from dataclasses import dataclass
from uuid import UUID
from todo_rpg.application.dto.sentinel_types import Unset


@dataclass
class UserRankReadDTO:
    id: UUID
    user_id: UUID
    title: str


@dataclass
class UserRankCreateDTO:
    title: str


@dataclass
class UserRankUpdateDTO:
    title: str | Unset
