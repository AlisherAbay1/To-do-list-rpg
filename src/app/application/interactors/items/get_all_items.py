from src.app.application.interfaces.repositories_interfaces import ItemRepositoryProtocol

class GetAllItemsInteractor:
    def __init__(self, repo: ItemRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, limit: int, offset: int):
        Items = await self.repo.get_all_items(limit, offset)
        return Items