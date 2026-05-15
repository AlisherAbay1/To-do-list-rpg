from uuid import UUID

from src.app.application.interfaces.repositories_interfaces import (
    ItemRepositoryProtocol,
)
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.exceptions import (
    SessionNotFoundError,
    ItemNotFoundError,
    AccessDeniedError,
)


class DeleteCurrentUserSkillRequirementInteractor:
    def __init__(
        self,
        repo: ItemRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        transaction: TransactionProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, item_id: UUID, skill_id: UUID, session_token: str):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        item = await self.repo.get_item_by_id(item_id)
        if item is None:
            raise ItemNotFoundError()
        if item.user_id != user_id:
            raise AccessDeniedError()
        await self.repo.delete_requirement(item_id=item_id, skill_id=skill_id)
        await self.transaction.commit()
