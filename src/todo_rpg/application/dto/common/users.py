from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass(slots=True)
class UserDTO:
    id: UUID
    username: str
    email: str
    password: str
    lvl: int
    xp: int
    gold: int
    timezone: str
    language: str
    is_admin: bool = False
    current_rank_id: Optional[UUID] = None
    profile_picture: Optional[str] = None


@dataclass(slots=True)
class CreateUserDTO:
    username: str
    email: str
    password: str


@dataclass(slots=True)
class SignInDTO:
    username_or_email: str
    password: str


@dataclass(slots=True)
class UserAuthDTO:
    username: str
    email: str
    session_token: str


@dataclass(slots=True)
class UserEmailDTO:
    new_email: str
    password: str


@dataclass(slots=True)
class UserPasswordDTO:
    old_password: str
    new_password: str


@dataclass(slots=True)
class UserStatsDTO:
    lvl: int
    xp: int
    xp_to_next_level: int
    gold: int
