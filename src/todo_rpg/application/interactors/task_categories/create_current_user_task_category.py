from todo_rpg.application.interfaces import SessionRepositoryProtocol, UoWProtocol
from todo_rpg.application.exceptions import SessionNotFoundError
from todo_rpg.domain import TaskCategory
from todo_rpg.application.dto import CreateTaskCategoryDTO, TaskCategoryDTO
from todo_rpg.application.mappers.common import TaskCategoriesMapper


class CreateCurrentUserTaskCategoryInteractor:
    def __init__(
        self, session_repo: SessionRepositoryProtocol, uow: UoWProtocol
    ) -> None:
        self.session_repo = session_repo
        self.uow = uow

    async def __call__(
        self, session_token: str, dto: CreateTaskCategoryDTO
    ) -> TaskCategoryDTO:
        user_id = await self.session_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        task_category = TaskCategory(user_id=user_id, title=dto.title, color=dto.color)
        output_dto = TaskCategoriesMapper.to_dto(task_category)
        self.uow.add(task_category)
        await self.uow.commit()
        return output_dto
