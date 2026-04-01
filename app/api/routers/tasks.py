from fastapi import APIRouter, Depends, Cookie, HTTPException
from pydantic import UUID7
from app.schemas import TaskSchemaCreate, TaskSchemaRead, TaskCreateDTO, \
                        TaskFilterParams, TaskSortParams, TaskFilterParamsDTO, \
                        TaskSortParamsDTO, TaskSchemaReadable, TaskWithSkillsAndItemsSchemaRead, \
                        TaskSchemaUpdate, TaskUpdateDTO
from app.repositories import TaskRepository, RedisRepository, TransactionAlchemyManager, TaskHistoryRepository
from app.services.interactors import GetAllTasksInteractor, CreateCurrentUserTaskInteractor, GetCurentUserTasksInteractor, \
                                     GetTaskInteractor, DeleteTaskInteractor, CompleteTaskInteractor, \
                                     UpdateTaskInteractor, UncompleteTaskInteractor
from app.core.database import get_local_session
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.core.redis_config import get_redis_session
from app.schemas.sentinel_types import UNSET

router = APIRouter(prefix="/tasks")

# admin
@router.get("", response_model=list[TaskSchemaRead])
async def get_all_tasks(filters: TaskFilterParams = Depends(),
                        sorting: TaskSortParams = Depends(),
                        limit: int = 20, 
                        offset: int = 0, 
                        session: AsyncSession = Depends(get_local_session)):
    repo = TaskRepository(session)
    interactor = GetAllTasksInteractor(repo)
    filters_dto = TaskFilterParamsDTO(difficulty=filters.difficulty,
                                      priority=filters.priority, 
                                      type=filters.type, 
                                      repeat_frequency=filters.repeat_frequency, 
                                      deleted=filters.deleted)
    sorting_dto = TaskSortParamsDTO(sort_by=sorting.sort_by, 
                                    sort_order=sorting.sort_order)
    return await interactor(filters_dto, sorting_dto, limit, offset)

@router.post("/me", response_model=TaskSchemaReadable)
async def create_current_user_task(data: TaskSchemaCreate, 
                                   session_token = Cookie(None), 
                                   session: AsyncSession = Depends(get_local_session),
                                   cash_session: Redis = Depends(get_redis_session)):
    repo = TaskRepository(session)
    cash_repo = RedisRepository(cash_session)
    transaction = TransactionAlchemyManager(session)
    interactor = CreateCurrentUserTaskInteractor(repo, cash_repo, transaction)
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    dto = TaskCreateDTO(
        title=data.title, 
        description=data.description, 
        category_id=data.category_id,
        repeat_limit=data.repeat_limit,
        repeat_frequency=data.repeat_frequency,
        deadline=data.deadline,
        type=data.type, 
        difficulty=data.difficulty,
        priority=data.priority,
        custom_xp_reward=data.custom_xp_reward, 
        custom_gold_reward=data.custom_gold_reward, 
        related_skills=data.related_skills, 
        related_items=data.related_items
    )
    task = await interactor(session_token, dto)
    return task

@router.get("/me", response_model=list[TaskSchemaRead])
async def get_current_user_tasks(session_token = Cookie(None), 
                                 limit: int = 20, 
                                 offset: int = 0, 
                                 session: AsyncSession = Depends(get_local_session),
                                 cash_session: Redis = Depends(get_redis_session)):
    repo = TaskRepository(session)
    cash_repo = RedisRepository(cash_session)
    interactor = GetCurentUserTasksInteractor(repo, cash_repo)
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_token, limit, offset)

@router.get("/{task_id}", response_model=TaskWithSkillsAndItemsSchemaRead)
async def get_task(task_id: UUID7, 
                   get_related_skills: bool, 
                   get_related_items: bool,
                   session: AsyncSession = Depends(get_local_session)):
    repo = TaskRepository(session)
    interactor = GetTaskInteractor(repo)
    return await interactor(task_id, get_related_skills, get_related_items)

@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: UUID7,
                      session: AsyncSession = Depends(get_local_session)):
    repo = TaskRepository(session)
    transaction = TransactionAlchemyManager(session)
    interactor = DeleteTaskInteractor(repo, transaction)
    await interactor(task_id)

@router.patch("/{task_id}/complete", response_model=TaskSchemaReadable) 
async def complete_task(task_id: UUID7, 
                        session_token = Cookie(None), 
                        session: AsyncSession = Depends(get_local_session), 
                        cash_session: Redis = Depends(get_redis_session)): 
    repo = TaskRepository(session)
    cash_repo = RedisRepository(cash_session)
    transaction = TransactionAlchemyManager(session)
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    interactor = CompleteTaskInteractor(repo, cash_repo, transaction)
    return await interactor(task_id, session_token)

@router.patch("/{task_id}/uncomplete", response_model=TaskSchemaReadable) 
async def uncomplete_task(task_id: UUID7, 
                        session_token = Cookie(None), 
                        session: AsyncSession = Depends(get_local_session), 
                        cash_session: Redis = Depends(get_redis_session)): 
    task_repo = TaskRepository(session)
    task_history_repo = TaskHistoryRepository(session)
    cash_repo = RedisRepository(cash_session)
    transaction = TransactionAlchemyManager(session)
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    interactor = UncompleteTaskInteractor(task_repo, task_history_repo, cash_repo, transaction)
    return await interactor(task_id, session_token)

@router.patch("/{task_id}", response_model=TaskSchemaReadable)
async def patch_task(task_id: UUID7, 
                     data: TaskSchemaUpdate, 
                     session_token = Cookie(None), 
                     session: AsyncSession = Depends(get_local_session), 
                     cash_session: Redis = Depends(get_redis_session)):
    repo = TaskRepository(session)
    cash_repo = RedisRepository(cash_session)
    transaction = TransactionAlchemyManager(session)
    if session_token is None:
        raise HTTPException(401, "Not authenticated")
    interactor = UpdateTaskInteractor(repo, cash_repo, transaction)
    clean_data = data.model_dump(exclude_unset=True)
    dto = TaskUpdateDTO(
        title=clean_data.get("title") or UNSET,
        description=clean_data.get("description", UNSET),
        category_id=clean_data.get("category_id", UNSET),
        repeat_limit=clean_data.get("repeat_limit", UNSET),
        repeat_frequency=clean_data.get("repeat_frequency", UNSET),
        deadline=clean_data.get("deadline", UNSET),
        type=clean_data.get("type", UNSET),
        difficulty=clean_data.get("difficulty", UNSET),
        priority=clean_data.get("priority", UNSET),
        custom_xp_reward=clean_data.get("custom_xp_reward", UNSET),
        custom_gold_reward=clean_data.get("custom_gold_reward", UNSET),
        deleted=clean_data.get("deleted") or UNSET,
    )
    return await interactor(task_id, dto, session_token)