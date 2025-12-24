from fastapi import APIRouter, HTTPException
from pydantic import UUID7
from app.schemas import UserSchemaCreate

router = APIRouter(prefix="/users")

@router.get("")
def get_all_users(limit: int = 20, offset: int = 0):
    pass

@router.get("/me")
def get_current_user():
    pass

@router.patch("/me")
def update_current_user():
    pass

@router.delete("/me")
def delete_current_user():
    pass

@router.get("/{user_id}")
def get_user(user_id: UUID7):
    pass

@router.patch("/{user_id}")
def update_user(user_id: UUID7):
    pass

@router.delete("/{user_id}")
def delete_user(user_id: UUID7):
    pass

