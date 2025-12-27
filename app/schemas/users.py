from typing import Optional
from pydantic import BaseModel, EmailStr, UUID7, ConfigDict, field_validator
from fastapi import HTTPException
from re import match

class UserSchemaRead(BaseModel):
    id: UUID7
    username: str
    email: EmailStr
    password: str
    lvl: int = 1
    xp: int = 0
    is_admin: bool = False
    current_rank_id: Optional[UUID7] = None
    profile_picture: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserSchemaCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    lvl: int = 1
    xp: int = 0
    is_admin: bool = False
    current_rank_id: Optional[UUID7] = None
    profile_picture: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserSchemaPatch(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    lvl: int = 1
    xp: int = 0
    is_admin: bool = False
    current_rank_id: Optional[UUID7] = None
    profile_picture: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserSchemaCreateAuth(BaseModel):
    id: UUID7
    username: str
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)
        
    @field_validator("username")
    def has_valid_chars_schema(cls, username: str):
        pattern = r"^[a-zA-Z][a-zA-Z0-9!#$%^&*_-]+$" 
        if match(pattern, username):
            return username
        raise HTTPException(500, "You should use only english chars, !, @, #, $, %, ^, &, *, _, -.")
    
    @field_validator("username")
    def is_correct_lenght_schema(cls, username: str):
        if len(username) > 3 and len(username) < 16:
            return username
        raise HTTPException(500, "Username should be at least 3 chars and less than 16.")
    
    @field_validator("password")
    def is_lenght_correct_schema(cls, password: str):
        if len(password) > 3 and len(password) < 50:
            return password
        raise HTTPException(500, "Username should be at least 8 chars and less than 50.")

class RankSchema(BaseModel):
    id: UUID7
    user_id: UUID7
    title: str

