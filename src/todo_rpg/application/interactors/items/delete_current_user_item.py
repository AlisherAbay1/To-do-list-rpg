from uuid import UUID

from todo_rpg.application.interfaces.repositories_interfaces import (
    ItemRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.exceptions import SessionNotFoundError, ItemNotFoundError


class DeleteCurrentUserItemInteractor:
    def __init__(
        self,
        repo: ItemRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(self, item_id: UUID, session_token: str):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        item = await self.repo.get_item_by_id(item_id)
        if item is None:
            raise ItemNotFoundError()
        item.delete()
        await self.uow.commit()
