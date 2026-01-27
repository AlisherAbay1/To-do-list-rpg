from app.repositories.interfaces import ItemRepositoryProtocol, RedisRepositoryProtocol
from app.models import Item
from app.schemas.dto import ItemCreateOrUpdateDTO
from app.exceptions import ItemNotFoundError

class GetAllItemsInteractor:
    def __init__(self, repo: ItemRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, limit: int, offset: int):
        Items = await self.repo.get_all_items(limit, offset)
        return Items

class GetCurrentUserItemsInteractor:
    def __init__(self, repo: ItemRepositoryProtocol, cash_repo: RedisRepositoryProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, session_id: str, limit: int, offset: int):
        user_id = await self.cash_repo.get_user_id_by_session_id(session_id)
        items = await self.repo.get_items_by_user_id(user_id, limit, offset)
        return items

class CreateCurrentUserItemInteractor:
    def __init__(self, repo: ItemRepositoryProtocol, cash_repo: RedisRepositoryProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, session_id: str, dto: ItemCreateOrUpdateDTO):
        user_id = await self.cash_repo.get_user_id_by_session_id(session_id)
        user = Item(
            user_id=user_id, 
            title=dto.title, 
            description=dto.description, 
            amount=dto.amount
        )
        self.repo.save(user)
        return dto

class GetItemInteractor:
    def __init__(self, repo: ItemRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, item_id):
        item = await self.repo.get_item_by_id(item_id)
        return item

class DeleteItemInteractor:
    def __init__(self, repo: ItemRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, item_id):
        item = await self.repo.get_item_by_id(item_id)
        if item is None:
            raise ItemNotFoundError()
        await self.repo.delete(item)
        return item