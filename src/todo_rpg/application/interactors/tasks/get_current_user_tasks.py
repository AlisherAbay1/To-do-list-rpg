from todo_rpg.application.mappers.common import TaskMapper
from todo_rpg.application.dto import TaskDetailDTO
from todo_rpg.application.exceptions import SessionNotFoundError
from todo_rpg.application.interfaces import (
    TaskRepositoryProtocol,
    SessionRepositoryProtocol,
)


class GetCurrentUserTasksInteractor:
    def __init__(
        self, repo: TaskRepositoryProtocol, session_repo: SessionRepositoryProtocol
    ) -> None:
        self.repo = repo
        self.session_repo = session_repo

    async def __call__(
        self, session_token, limit: int, offset: int
    ) -> list[TaskDetailDTO]:
        user_id = await self.session_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        tasks = await self.repo.get_tasks_by_user_id(user_id, limit, offset)
        return TaskMapper.to_list_detail_dto(tasks)
