from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import UUID7
from app.schemas import TaskSchemaCreate, TaskSchemaRead, TaskSchemaPatch, UserSchemaRead
from app.repositories import TaskCRUD, UserCRUD
from app.models import Task, User
from app.core.session import get_user_by_session
from app.core.dto import model_to_dto, models_to_dtos
from app.core.session import get_user_id_by_session

router = APIRouter(prefix="/tasks")

# admin
@router.get("")
async def get_all_tasks(limit: int = 20, offset: int = 0, crud: TaskCRUD = Depends()):
    selected = crud.select_many(limit, offset)
    return models_to_dtos(await selected, TaskSchemaRead)

@router.post("/me")
async def create_current_user_task(data: TaskSchemaCreate, request: Request, crud: TaskCRUD = Depends()):
    info = data.model_dump()
    info["user_id"] = await get_user_id_by_session(request)
    return model_to_dto(await crud.insert(**info), TaskSchemaRead)

@router.get("/me")
async def get_current_user_tasks(request: Request, limit: int = 20, offset: int = 0, crud: TaskCRUD = Depends()):
    current_user_id = await get_user_id_by_session(request)
    selected = crud.select_many(limit, offset, Task.user_id == current_user_id)
    return models_to_dtos(await selected, TaskSchemaRead)

@router.get("/{task_id}")
async def get_task(task_id: UUID7, request: Request, crud: TaskCRUD = Depends()):
    selected = crud.select(
        Task.user_id == await get_user_by_session(request), 
        Task.id == task_id
    )
    return model_to_dto(await selected, TaskSchemaRead) 

@router.patch("/{task_id}")
async def update_task(task_id: UUID7, request: Request, data: TaskSchemaPatch, crud: TaskCRUD = Depends()):
    info = data.model_dump(exclude_unset=True)
    updated = crud.update(
        Task.user_id == await get_user_by_session(request), 
        Task.id == task_id,  
        **info
    )
    return model_to_dto(await updated, TaskSchemaRead)

@router.delete("/{task_id}")
async def delete_task(task_id: UUID7, request: Request, crud: TaskCRUD = Depends()):
    deleted = crud.delete(
        Task.user_id == await get_user_id_by_session(request), 
        Task.id == task_id
    )
    return model_to_dto(await deleted, TaskSchemaRead)

@router.patch("/{task_id}/complete")
async def complete_task(task_id: UUID7, request: Request, task_crud: TaskCRUD = Depends(), user_crud: UserCRUD = Depends()):
    user_id = await get_user_id_by_session(request)
    updated_task = task_crud.update(
        Task.user_id == user_id, 
        Task.id == task_id, 
        is_done=True
    )
    get_xp = TaskSchemaRead.model_validate(await updated_task, from_attributes=True).xp
    selected_user = user_crud.select(
        User.id == user_id
    )
    user_info = UserSchemaRead.model_validate(await selected_user, from_attributes=True)
    user_info.xp += get_xp
    updated_user = user_crud.update(
        User.id == user_id,
        **user_info.model_dump()
    )
    return model_to_dto(await updated_user, UserSchemaRead)