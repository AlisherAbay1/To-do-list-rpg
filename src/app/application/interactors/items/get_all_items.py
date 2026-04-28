from src.app.application.interfaces.repositories_interfaces import \
    ItemRepositoryProtocol
from src.app.application.mappers import ItemMapper

class GetAllItemsInteractor:
    def __init__(self, repo: ItemRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, limit: int, offset: int):
        items = await self.repo.get_all_items(limit, offset)
        dtos = ItemMapper.to_list_dto(items)
        return dtos