from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from app.enums import RepeatTypes

@dataclass(slots=True)
class UserDTO:
    username: str
    email: str
    password: str
    lvl: int = 1
    xp: int = 0
    is_admin: bool = False
    current_rank_id: Optional[UUID] = None
    profile_picture: Optional[str] = None

@dataclass(slots=True)
class CreateUserDTO:
    username: str
    email: str
    password: str

@dataclass(slots=True)
class LoginIdentifierDTO:
    username_or_email: str
    password: str

@dataclass(slots=True)
class CreateUserResultDTO:
    username: str
    email: str
    session_id: str

@dataclass(slots=True)
class UserEmailDTO:
    new_email: str
    password: str

@dataclass(slots=True)
class UserPasswordDTO:
    old_password: str
    new_password: str

@dataclass(slots=True)
class TaskCreateOrUpdateDTO:
    title: Optional[str]
    description: Optional[str]
    xp: Optional[int]
    is_done: Optional[bool]
    repeat_limit: Optional[int]
    repeat_type: Optional[RepeatTypes]

@dataclass(slots=True)
class SkillCreateOrUpdateDTO:
    title: Optional[str]
    description: Optional[str]
    ico: Optional[str]
    lvl: Optional[int]
    xp: Optional[int]

@dataclass(slots=True)
class ItemCreateOrUpdateDTO:
    title: Optional[str]
    description: Optional[str]
    amount: Optional[int]