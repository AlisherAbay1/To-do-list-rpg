from todo_rpg.application.exceptions import UserNotFoundError
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.repositories_interfaces import (
    UserRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import TransactionProtocol


class DeleteCurrentUserInteractor:
    def __init__(
        self,
        repo: UserRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        transaction: TransactionProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_token):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise UserNotFoundError()
        await self.repo.delete(user_id)
        await self.transaction.commit()
