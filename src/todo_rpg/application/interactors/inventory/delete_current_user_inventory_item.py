from todo_rpg.application.interfaces import (
    UoWProtocol,
    SessionRepositoryProtocol,
    InventoryRepositoryProtocol,
)
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    InventoryItemNotFoundError,
    AccessDeniedError,
)
from uuid import UUID


class DeleteCurrentUserInventoryItemInteractor:
    def __init__(
        self,
        repo: InventoryRepositoryProtocol,
        session_repo: SessionRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.session_repo = session_repo
        self.uow = uow

    async def __call__(self, inventory_item_id: UUID, session_token: str) -> None:
        user_id = await self.session_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        inventory_item = await self.repo.get_inventory_item_by_id(inventory_item_id)
        if inventory_item is None:
            raise InventoryItemNotFoundError()
        if inventory_item.user_id != user_id:
            raise AccessDeniedError()
        await self.repo.delete(inventory_item)
        await self.uow.commit()
