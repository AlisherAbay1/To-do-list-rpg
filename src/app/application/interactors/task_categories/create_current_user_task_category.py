from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.exceptions import SessionNotFoundError
from src.app.domain import TaskCategory
from src.app.application.dto.task_categories import CreateTaskCategoryDTO
from src.app.application.mappers import TaskCategoriesMapper

class CreateCurrentUserTaskCategory:
    def  __init__(self, 
                  cash_repo: RedisRepositoryProtocol, 
                  transaction: TransactionProtocol) -> None:
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_token: str, dto: CreateTaskCategoryDTO):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        task_category = TaskCategory(
            user_id=user_id,
            title=dto.title, 
            color=dto.color 
        )
        output_dto = TaskCategoriesMapper.to_dto(task_category)
        await self.transaction.save(task_category)
        await self.transaction.commit()
        return output_dto