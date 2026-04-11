from src.app.application.interfaces.repositories_interfaces import UserRepositoryProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.exceptions import SessionNotFoundError, UserNotFoundError
from uuid import UUID

class DeleteCurrentUserInteractor:
    def __init__(self, repo: UserRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_token):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.repo.get_user(UUID(user_id))
        if not user:
            raise UserNotFoundError()
        await self.repo.delete(user)
        await self.transaction.commit()