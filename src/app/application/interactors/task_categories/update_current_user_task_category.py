from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.interfaces.repositories_interfaces import TaskCategoriesRepositoryProtocol
from src.app.application.exceptions import SessionNotFoundError
from src.app.application.dto.task_categories import UpdateTaskCategoryDTO, TaskCategoryDTO
from uuid import UUID
from src.app.application.dto.sentinel_types import Unset
from src.app.application.exceptions import AccessDeniedError, TaskCategoryNotFoundError
from src.app.application.mappers import TaskCategoriesMapper

class UpdateCurrentUserTaskCategory:
    def  __init__(self, 
                  repo: TaskCategoriesRepositoryProtocol,
                  cash_repo: RedisRepositoryProtocol, 
                  transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, task_category_id: UUID, dto: UpdateTaskCategoryDTO, session_token: str) -> TaskCategoryDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        task_category = await self.repo.get_task_category_by_id(task_category_id)
        if task_category is None:
            raise TaskCategoryNotFoundError()
        if task_category.user_id != user_id:
            raise AccessDeniedError()
        if not isinstance(dto.title, Unset):
            task_category.title = dto.title
        if not isinstance(dto.color, Unset):
            task_category.color = dto.color
        output_dto = TaskCategoriesMapper.to_dto(task_category)
        await self.transaction.commit()
        return output_dto