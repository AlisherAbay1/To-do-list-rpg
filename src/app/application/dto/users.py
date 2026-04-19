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
    session_token: str

@dataclass(slots=True)
class UserEmailDTO:
    new_email: str
    password: str

@dataclass(slots=True)
class UserPasswordDTO:
    old_password: str
    new_password: str
