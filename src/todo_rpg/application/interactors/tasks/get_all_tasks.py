from todo_rpg.application.dto import TaskFilterParamsDTO, TaskSortParamsDTO
from todo_rpg.application.interfaces import (
    TaskRepositoryProtocol,
    UserRepositoryProtocol,
    RedisRepositoryProtocol,
)
from todo_rpg.application.mappers import TaskMapper
from todo_rpg.application.dto import TaskDetailDTO
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    UserNotFoundError,
    AccessDeniedError,
)


class GetAllTasksInteractor:
    def __init__(
        self,
        task_repo: TaskRepositoryProtocol,
        user_repo: UserRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
    ) -> None:
        self.task_repo = task_repo
        self.user_repo = user_repo
        self.cash_repo = cash_repo

    async def __call__(
        self,
        session_token: str,
        filters: TaskFilterParamsDTO,
        sorting: TaskSortParamsDTO,
        limit: int,
        offset: int,
    ) -> list[TaskDetailDTO]:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.user_repo.get_user(user_id)
        if user is None:
            raise UserNotFoundError()
        if not user.is_admin:
            raise AccessDeniedError()
        tasks = await self.task_repo.get_all_tasks(filters, sorting, limit, offset)
        dtos = TaskMapper.to_list_detail_dto(tasks)
        return dtos
