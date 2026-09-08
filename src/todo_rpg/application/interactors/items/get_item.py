from todo_rpg.application.exceptions import ItemNotFoundError
from todo_rpg.application.interfaces import (
    ItemRepositoryProtocol,
)
from todo_rpg.application.mappers.common import ItemMapper
from todo_rpg.application.dto import ItemDTO
from uuid import UUID


class GetItemInteractor:
    def __init__(self, repo: ItemRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, item_id: UUID) -> ItemDTO:
        item = await self.repo.get_item_by_id(item_id)
        if item is None:
            raise ItemNotFoundError()
        dto = ItemMapper.to_dto(item)
        return dto
