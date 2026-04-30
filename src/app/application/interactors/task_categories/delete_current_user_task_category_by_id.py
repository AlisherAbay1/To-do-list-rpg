from src.app.application.interfaces.repositories_interfaces import TaskCategoriesRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from uuid import UUID
from src.app.application.exceptions import SessionNotFoundError

class DeleteCurrentUserTaskCategoryById:
    def __init__(self, 
                 repo: TaskCategoriesRepositoryProtocol, 
                 cash_repo: RedisRepositoryProtocol, 
                 transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_id: str, task_category_id: UUID) -> None:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_id)
        if user_id is None:
            raise SessionNotFoundError()
        await self.repo.delete_current_user_task_category_by_id(task_category_id)
        await self.transaction.commit()
