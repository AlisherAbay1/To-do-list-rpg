from uuid import UUID

from src.app.application.interfaces.repositories_interfaces import \
    ItemRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import \
    TransactionProtocol
from src.app.application.interfaces.cash_interfaces import \
    RedisRepositoryProtocol
from src.app.application.exceptions import SessionNotFoundError, ItemNotFoundError

class DeleteCurrentUserItemInteractor:
    def __init__(self, 
                 repo: ItemRepositoryProtocol, 
                 cash_repo: RedisRepositoryProtocol,
                 transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, item_id: UUID, session_token: str):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        item = await self.repo.get_item_by_id(item_id)
        if item is None:
            raise ItemNotFoundError()
        item.delete()
        await self.transaction.commit()