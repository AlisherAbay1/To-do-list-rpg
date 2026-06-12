from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol
from todo_rpg.application.exceptions import SessionNotFoundError
from todo_rpg.domain import TaskCategory
from todo_rpg.application.dto import CreateTaskCategoryDTO
from todo_rpg.application.mappers.common import TaskCategoriesMapper


class CreateCurrentUserTaskCategory:
    def __init__(self, cash_repo: RedisRepositoryProtocol, uow: UoWProtocol) -> None:
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(self, session_token: str, dto: CreateTaskCategoryDTO):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        task_category = TaskCategory(user_id=user_id, title=dto.title, color=dto.color)
        output_dto = TaskCategoriesMapper.to_dto(task_category)
        await self.uow.add(task_category)
        await self.uow.commit()
        return output_dto
