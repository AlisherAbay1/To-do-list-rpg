from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from fastapi import HTTPException
from re import match
from uuid import UUID

class UserSchemaRead(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    lvl: int
    xp: int
    is_admin: bool
    current_rank_id: Optional[UUID]
    profile_picture: Optional[str]
    gold: int
    language: str
    timezone: str

    model_config = ConfigDict(from_attributes=True)

class UserSchemaCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    lvl: int = 1
    xp: int = 0
    is_admin: bool = False
    current_rank_id: Optional[UUID] = None
    profile_picture: Optional[str] = None
    gold: int = 0
    language: str = "eng"
    timezone: str = "UTC"

    model_config = ConfigDict(from_attributes=True)

class UserSchemaPatchEmail(BaseModel):
    new_email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("password")
    def is_lenght_correct_schema(cls, password: str):
        if len(password) > 3 and len(password) < 50:
            return password
        raise HTTPException(500, "Password should be at least 8 chars and less than 50.")

class UserSchemaPatchPassword(BaseModel):
    old_password: str
    new_password: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("new_password")
    def is_lenght_correct_schema(cls, password: str):
        if len(password) > 3 and len(password) < 50:
            return password
        raise HTTPException(500, "Password should be at least 8 chars and less than 50.")

class UserSignInSchema(BaseModel):
    username_or_email: str
    password: str

    model_config = ConfigDict(from_attributes=True)

class UserSuccessAuthSchema(BaseModel):
    username: str
    email: str
    message: str

class UserNewEmailSchema(BaseModel):
    new_email: str
    message: str

class UserSchemaCreateAuth(BaseModel):
    username: str
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)
        
    @field_validator("username")
    def has_valid_chars_schema(cls, username: str):
        pattern = r"^[a-zA-Z][a-zA-Z0-9!#$%^&*_-]+$" 
        if match(pattern, username):
            return username
        raise HTTPException(500, "You should use only english chars, numbers, !, @, #, $, %, ^, &, *, _, -.")
    
    @field_validator("username")
    def is_correct_lenght_schema(cls, username: str):
        if len(username) > 3 and len(username) < 16:
            return username
        raise HTTPException(500, "Username should be at least 3 chars and less than 16.")
    
    @field_validator("password")
    def is_lenght_correct_schema(cls, password: str):
        if len(password) > 3 and len(password) < 50:
            return password
        raise HTTPException(500, "Password should be at least 8 chars and less than 50.")

class RankSchema(BaseModel):
    id: UUID
    user_id: UUID
    title: str

