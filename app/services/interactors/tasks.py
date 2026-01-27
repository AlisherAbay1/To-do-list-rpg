from app.repositories.interfaces import TaskRepositoryProtocol, RedisRepositoryProtocol
from app.exceptions import TaskNotFoundError, UserNotFoundError, TaskAlreadyDoneError
from app.schemas.dto import TaskCreateOrUpdateDTO
from app.models import Task
from uuid import UUID

class GetAllTasksInteractor:
    def __init__(self, repo: TaskRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, limit, offset):
        tasks = await self.repo.get_all_tasks(limit, offset)
        return list(tasks)

class CreateCurrentUserTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, cash_repo: RedisRepositoryProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, session_id, dto: TaskCreateOrUpdateDTO):
        user_id = await self.cash_repo.get_user_id_by_session_id(session_id)
        task = Task(
            user_id=user_id,
            title=dto.title,
            description=dto.description,
            xp=dto.xp, 
            is_done=dto.is_done, 
            repeat_limit=dto.repeat_limit,
            repeat_type=dto.repeat_type
        )
        self.repo.save(task)

class GetCurentUserTasksInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, cash_repo: RedisRepositoryProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, session_id, limit: int, offset: int):
        user_id = await self.cash_repo.get_user_id_by_session_id(session_id)
        tasks = await self.repo.get_tasks_by_user_id(user_id, limit, offset)
        return tasks

class GetTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, task_id: UUID):
        task = await self.repo.get_task_by_id(task_id)
        return task

class CompleteTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, task_id: UUID):
        task = await self.repo.get_task_with_user(task_id)
        if task is None:
            raise TaskNotFoundError()
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
        return task

class DeleteTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, task_id: UUID):
        task = await self.repo.get_task_by_id(task_id)
        if task is None:
            raise TaskNotFoundError()
        await self.repo.delete(task)