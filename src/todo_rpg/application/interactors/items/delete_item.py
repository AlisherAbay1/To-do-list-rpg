from uuid import UUID

from todo_rpg.application.interfaces.repositories_interfaces import (
    ItemRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol


class DeleteItemInteractor:
    def __init__(self, repo: ItemRepositoryProtocol, uow: UoWProtocol) -> None:
        self.repo = repo
        self.uow = uow

    async def __call__(self, item_id: UUID):
        await self.repo.delete(item_id)
        await self.uow.commit()
