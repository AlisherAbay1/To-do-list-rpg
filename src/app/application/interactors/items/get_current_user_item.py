from src.app.application.exceptions import SessionNotFoundError
from src.app.application.interfaces.cash_interfaces import \
    RedisRepositoryProtocol
from src.app.application.interfaces.repositories_interfaces import \
    ItemRepositoryProtocol
from src.app.application.mappers.common import ItemMapper
from uuid import UUID
from src.app.application.exceptions import ItemNotFoundError, AccessDeniedError

class GetCurrentUserItemInteractor:
    def __init__(self, repo: ItemRepositoryProtocol, cash_repo: RedisRepositoryProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, task_id: UUID, session_token: str):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        item = await self.repo.get_item_by_id(task_id)
        if item is None:
            raise ItemNotFoundError()
        if item.user_id != user_id:
            raise AccessDeniedError()