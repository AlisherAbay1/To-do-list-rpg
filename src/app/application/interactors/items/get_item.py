from src.app.application.interfaces.repositories_interfaces import ItemRepositoryProtocol
from src.app.application.exceptions import ItemNotFoundError

class GetItemInteractor:
    def __init__(self, repo: ItemRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, item_id):
        item = await self.repo.get_item_by_id(item_id)
        if item is None:
            raise ItemNotFoundError()
        return item