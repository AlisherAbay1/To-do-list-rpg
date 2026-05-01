from src.app.application.exceptions import SessionNotFoundError
from src.app.application.interfaces.cash_interfaces import \
    RedisRepositoryProtocol
from src.app.application.interfaces.repositories_interfaces import \
    ItemRepositoryProtocol
from src.app.application.mappers.common import ItemMapper

class GetCurrentUserItemsInteractor:
    def __init__(self, repo: ItemRepositoryProtocol, cash_repo: RedisRepositoryProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, session_token: str, limit: int, offset: int):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        items = await self.repo.get_items_by_user_id(user_id, limit, offset)
        dtos = ItemMapper.to_list_dto(items)
        return dtos