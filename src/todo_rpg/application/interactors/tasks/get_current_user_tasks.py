from todo_rpg.application.mappers.common import TaskMapper
from todo_rpg.application.dto import TaskDetailDTO
from todo_rpg.application.exceptions import SessionNotFoundError
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.repositories_interfaces import (
    TaskRepositoryProtocol,
)


class GetCurentUserTasksInteractor:
    def __init__(
        self, repo: TaskRepositoryProtocol, cash_repo: RedisRepositoryProtocol
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(
        self, session_token, limit: int, offset: int
    ) -> list[TaskDetailDTO]:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        tasks = await self.repo.get_tasks_by_user_id(user_id, limit, offset)
        return TaskMapper.to_list_detail_dto(tasks)
