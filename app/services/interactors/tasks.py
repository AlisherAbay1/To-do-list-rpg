from app.repositories.interfaces import TaskRepositoryProtocol, RedisRepositoryProtocol, TransactionProtocol
from app.exceptions import TaskNotFoundError, TaskAlreadyDoneError, SessionNotFoundError, \
                           TaskAccessDeniedError
from app.schemas.dto import TaskCreateDTO, TaskDTO, TaskUpdateDTO
from app.models import Task
from uuid import UUID
from uuid_utils import uuid7

class GetAllTasksInteractor:
    def __init__(self, repo: TaskRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, limit, offset):
        tasks = await self.repo.get_all_tasks(limit, offset)
        return list(tasks)

class CreateCurrentUserTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_id, dto: TaskCreateDTO):
        user_id = await self.cash_repo.get_user_id_by_session_id(session_id)
        if user_id is None:
            raise SessionNotFoundError()
        task_id=uuid7()
        task = Task(
            id=task_id,
            user_id=user_id,
            title=dto.title,
            description=dto.description,
            xp=dto.xp, 
            is_done=dto.is_done, 
            repeat_limit=dto.repeat_limit,
            repeat_type=dto.repeat_type
        )
        self.repo.save(task)
        await self.transaction.commit()
        return TaskDTO(
            id=UUID(str(task_id)),
            user_id=UUID(str(user_id)),
            title=dto.title,
            description=dto.description,
            xp=dto.xp, 
            is_done=dto.is_done, 
            repeat_limit=dto.repeat_limit,
            repeat_type=dto.repeat_type
        )

class GetCurentUserTasksInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, cash_repo: RedisRepositoryProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, session_id, limit: int, offset: int):
        user_id = await self.cash_repo.get_user_id_by_session_id(session_id)
        if user_id is None:
            raise SessionNotFoundError()
        tasks = await self.repo.get_tasks_by_user_id(UUID(user_id), limit, offset)
        return tasks

class GetTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, task_id: UUID):
        task = await self.repo.get_task_by_id(task_id)
        if task is None:
            raise TaskNotFoundError()
        return task

class CompleteTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, task_id: UUID, session_id: str):
        task = await self.repo.get_task_with_user(task_id)
        user_id = await self.cash_repo.get_user_id_by_session_id(session_id)
        if user_id is None:
            raise SessionNotFoundError()
        if task is None:
            raise TaskNotFoundError()
        if task.user_id != UUID(user_id):
            raise TaskAccessDeniedError()
        if task.is_done:
            raise TaskAlreadyDoneError()
        if task.repeat_limit is not None:
            if task.repeat_limit > 0:
                task.repeat_limit -= 1
                if task.repeat_limit == 0:
                    task.is_done = True
        else: 
            task.is_done = True
        
        task.user.xp += task.xp
        task.user.lvl = task.user.xp // 1000
        dto = TaskDTO(
            id=task.id,
            user_id=task.user_id,
            title=task.title, 
            description=task.description, 
            xp=task.xp, 
            is_done=task.is_done,
            repeat_limit=task.repeat_limit, 
            repeat_type=task.repeat_type
        )
        await self.transaction.commit()
        return dto

class DeleteTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.transaction = transaction

    async def __call__(self, task_id: UUID):
        task = await self.repo.get_task_by_id(task_id)
        if task is None:
            raise TaskNotFoundError()
        await self.repo.delete(task)
        await self.transaction.commit()