from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Cookie, Depends, HTTPException
from pydantic import UUID7

from src.app.application.interactors import (
    CompleteTaskInteractor, CreateCurrentUserTaskInteractor,
    DeleteTaskInteractor, GetAllTasksInteractor, GetCurentUserTasksInteractor,
    GetDailyTasksBySessionTokenInteractor,
    GetDeletedTasksBySessionTokenInteractor, GetOverdueTasksInteractor,
    GetTaskInteractor, UncompleteTaskInteractor, UpdateCurrentUserTaskInteractor, 
    GetTodaysDeadlineInteractor)
from src.app.presentation.mappers import TaskSchemaMapper
from src.app.presentation.schemas import (TaskFilterParams, TaskSchemaCreate,
                                          TaskSchemaRead, TaskSchemaReadable,
                                          TaskSchemaUpdate, TaskSortParams,
                                          TaskWithSkillsAndItemsSchemaRead,
                                          TaskWithUserAndSkillsSchema)

router = APIRouter(prefix="/tasks", route_class=DishkaRoute)

# admin
@router.get("", response_model=list[TaskSchemaRead])
async def get_all_tasks(interactor: FromDishka[GetAllTasksInteractor], 
                        filters: TaskFilterParams = Depends(),
                        sorting: TaskSortParams = Depends(),
                        limit: int = 20, 
                        offset: int = 0):
    filters_dto = TaskSchemaMapper.to_filter_params_dto(filters)
    sorting_dto = TaskSchemaMapper.to_sorting_params_dto(sorting)
    return await interactor(filters_dto, sorting_dto, limit, offset)

@router.get("/me", response_model=list[TaskSchemaRead])
async def get_current_user_tasks(interactor: FromDishka[GetCurentUserTasksInteractor], 
                                 session_token = Cookie(None), 
                                 limit: int = 20, 
                                 offset: int = 0):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token, limit, offset)

@router.get("/me/archived")
async def get_deleted_tasks_by_session_token(interactor: FromDishka[GetDeletedTasksBySessionTokenInteractor], 
                                       session_token = Cookie(None)):
    return await interactor(session_token)

@router.get("/me/daily")
async def get_daily_tasks_by_session_token(interactor: FromDishka[GetDailyTasksBySessionTokenInteractor], 
                                       session_token = Cookie(None)):
    return await interactor(session_token)

@router.get("/me/today")
async def get_todays_deadline_tasks_by_session_token(interactor: FromDishka[GetTodaysDeadlineInteractor], 
                                       session_token = Cookie(None)):
    return await interactor(session_token)

@router.get("/me/overdue")
async def get_overdue_tasks_by_session_token(interactor: FromDishka[GetOverdueTasksInteractor], 
                                       session_token = Cookie(None)):
    return await interactor(session_token)

@router.get("/{task_id}", response_model=TaskWithSkillsAndItemsSchemaRead)
async def get_task(task_id: UUID7, 
                   get_related_skills: bool, 
                   get_related_items: bool,
                   interactor: FromDishka[GetTaskInteractor]):
    return await interactor(task_id, get_related_skills, get_related_items)

@router.post("/me", response_model=TaskSchemaReadable)
async def create_current_user_task(interactor: FromDishka[CreateCurrentUserTaskInteractor], 
                                   data: TaskSchemaCreate, 
                                   session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = TaskSchemaMapper.to_create_dto(data)
    task = await interactor(session_token, dto)
    return task

@router.patch("/me/{task_id}/complete", response_model=TaskWithUserAndSkillsSchema) 
async def complete_task(interactor: FromDishka[CompleteTaskInteractor], 
                        task_id: UUID7, 
                        session_token = Cookie(None)): 
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(task_id, session_token)

@router.patch("/me/{task_id}/uncomplete", response_model=TaskWithUserAndSkillsSchema) 
async def uncomplete_task(interactor: FromDishka[UncompleteTaskInteractor], 
                          task_id: UUID7, 
                          session_token = Cookie(None)): 
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(task_id, session_token)

@router.patch("/me/{task_id}", response_model=TaskSchemaReadable)
async def patch_task(interactor: FromDishka[UpdateCurrentUserTaskInteractor], 
                     task_id: UUID7, 
                     data: TaskSchemaUpdate, 
                     session_token = Cookie(None)):
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = TaskSchemaMapper.to_update_dto(data)
    return await interactor(task_id, dto, session_token)

@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: UUID7,
                      interactor: FromDishka[DeleteTaskInteractor]):
    await interactor(task_id)