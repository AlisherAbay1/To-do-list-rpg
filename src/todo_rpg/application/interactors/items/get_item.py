from todo_rpg.application.exceptions import ItemNotFoundError
from todo_rpg.application.interfaces.repositories_interfaces import (
    ItemRepositoryProtocol,
)
from todo_rpg.application.mappers.common import ItemMapper


class GetItemInteractor:
    def __init__(self, repo: ItemRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, item_id):
        item = await self.repo.get_item_by_id(item_id)
        if item is None:
            raise ItemNotFoundError()
        dto = ItemMapper.to_dto(item)
        return dto
