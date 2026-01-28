from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import UUID7
from app.schemas import TaskSchemaCreate, TaskSchemaRead, TaskCreateOrUpdateDTO
from app.repositories import TaskRepository, RedisRepository, TransactionAlchemyManager
from app.services.interactors import GetAllTasksInteractor, CreateCurrentUserTaskInteractor, GetCurentUserTasksInteractor, \
                                    GetTaskInteractor, DeleteTaskInteractor, CompleteTaskInteractor
from app.core.database import get_local_session
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.core.redis_config import get_redis_session

router = APIRouter(prefix="/tasks")

# admin
@router.get("", response_model=list[TaskSchemaRead])
async def get_all_tasks(limit: int = 20, 
                        offset: int = 0, 
                        session: AsyncSession = Depends(get_local_session)):
    repo = TaskRepository(session)
    interactor = GetAllTasksInteractor(repo)
    return await interactor(limit, offset)

@router.post("/me", response_model=TaskSchemaRead, status_code=204)
async def create_current_user_task(data: TaskSchemaCreate, 
                                   request: Request, 
                                   session: AsyncSession = Depends(get_local_session),
                                   cash_session: Redis = Depends(get_redis_session)):
    repo = TaskRepository(session)
    cash_repo = RedisRepository(cash_session)
    transaction = TransactionAlchemyManager(session)
    interactor = CreateCurrentUserTaskInteractor(repo, cash_repo, transaction)
    session_id = request.cookies.get("session_id")
    if session_id is None:
        raise HTTPException(401, "Not authenticated")
    dto = TaskCreateOrUpdateDTO(
        title=data.title, 
        description=data.description, 
        xp=data.xp, 
        is_done=data.is_done,
        repeat_limit=data.repeat_limit,
        repeat_type=data.repeat_type
    )
    await interactor(session_id, dto)

@router.get("/me", response_model=TaskSchemaRead)
async def get_current_user_tasks(request: Request, 
                                 limit: int = 20, 
                                 offset: int = 0, 
                                 session: AsyncSession = Depends(get_local_session),
                                 cash_session: Redis = Depends(get_redis_session)):
    repo = TaskRepository(session)
    cash_repo = RedisRepository(cash_session)
    interactor = GetCurentUserTasksInteractor(repo, cash_repo)
    session_id = request.cookies.get("session_id")
    if session_id is None:
        raise HTTPException(401, "Not authenticated")
    return await interactor(session_id, limit, offset)

@router.get("/{task_id}", response_model=TaskSchemaRead)
async def get_task(task_id: UUID7, 
                   request: Request, 
                   session: AsyncSession = Depends(get_local_session)):
    repo = TaskRepository(session)
    interactor = GetTaskInteractor(repo)
    return await interactor(task_id)

@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: UUID7,
                      session: AsyncSession = Depends(get_local_session)):
    repo = TaskRepository(session)
    transaction = TransactionAlchemyManager(session)
    interactor = DeleteTaskInteractor(repo, transaction)
    await interactor(task_id)

@router.patch("/{task_id}/complete", response_model=TaskSchemaRead)
async def complete_task(task_id: UUID7,
                        session: AsyncSession = Depends(get_local_session)):
    repo = TaskRepository(session)
    transaction = TransactionAlchemyManager(session)
    interactor = CompleteTaskInteractor(repo, transaction)
    return await interactor(task_id)