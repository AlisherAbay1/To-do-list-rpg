from fastapi import APIRouter, HTTPException
from pydantic import UUID7
from app.schemas import TaskSchemaCreate

router = APIRouter(prefix="/tasks")

@router.get("")
def get_all_tasks(limit: int = 20, offset: int = 0):
    pass

@router.post("")
def create_task():
    pass

@router.get("/me")
def get_current_user_tasks(limit: int = 20, offset: int = 0):
    pass

@router.get("/{task_id}")
def get_task(task_id: UUID7):
    pass

@router.patch("/{task_id}")
def update_task(task_id: UUID7):
    pass

@router.delete("/{task_id}")
def delete_task(task_id: UUID7):
    pass

