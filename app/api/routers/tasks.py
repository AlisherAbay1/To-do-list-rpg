from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import UUID7
from app.schemas import TaskSchemaCreate, TaskSchemaRead, TaskSchemaPatch
from app.repositories.tasks import TaskCRUD
from app.models.tasks import Task
from app.core.session import get_user_by_session
from app.core.dto import model_to_dto, models_to_dtos
from app.core.session import get_user_id_by_session

router = APIRouter(prefix="/tasks")

@router.get("")
def get_all_tasks(limit: int = 20, offset: int = 0, crud: TaskCRUD = Depends()):
    selected = crud.select_many(limit, offset)
    return models_to_dtos(selected, TaskSchemaRead)

@router.post("")
def create_task(data: TaskSchemaCreate, request: Request, crud: TaskCRUD = Depends()):
    info = data.model_dump()
    info["user_id"] = get_user_id_by_session(request)
    return model_to_dto(crud.insert(**info), TaskSchemaRead)

@router.get("/me")
def get_current_user_tasks(request: Request, limit: int = 20, offset: int = 0, crud: TaskCRUD = Depends()):
    current_user_id = get_user_id_by_session(request)
    selected = crud.select_many(limit, offset, Task.user_id == current_user_id)
    return models_to_dtos(selected, TaskSchemaRead)

@router.get("/{task_id}")
def get_task(task_id: UUID7, crud: TaskCRUD = Depends()):
    selected = crud.select(Task.id == task_id)
    return model_to_dto(selected, TaskSchemaRead) 

@router.patch("/{task_id}")
def update_task(task_id: UUID7, data: TaskSchemaPatch, crud: TaskCRUD = Depends()):
    info = data.model_dump(exclude_unset=True)
    updated = crud.update(Task.id == task_id, **info)
    return model_to_dto(updated, TaskSchemaRead)

@router.delete("/{task_id}")
def delete_task(task_id: UUID7, crud: TaskCRUD = Depends()):
    deleted = crud.delete(Task.id == task_id)
    return model_to_dto(deleted, TaskSchemaRead)