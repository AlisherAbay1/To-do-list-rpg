from todo_rpg.application.exceptions import ItemNotFoundError
from todo_rpg.application.interfaces import (
    ItemRepositoryProtocol,
    SessionRepositoryProtocol,
)
from todo_rpg.application.mappers.common import ItemMapper
from todo_rpg.application.dto import ItemDTO
from uuid import UUID
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    UserNotFoundError,
    AccessDeniedError,
)


class GetItemInteractor:
    def __init__(
        self, repo: ItemRepositoryProtocol, session_repo: SessionRepositoryProtocol
    ) -> None:
        self.repo = repo
        self.session_repo = session_repo

    async def __call__(self, item_id: UUID, session_token: str) -> ItemDTO:
        user_id = await self.session_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.user_repo.get_user(user_id)
        if user is None:
            raise UserNotFoundError()
        if not user.is_admin:
            raise AccessDeniedError()

        item = await self.repo.get_item_by_id(item_id)
        if item is None:
            raise ItemNotFoundError()
        dto = ItemMapper.to_dto(item)
        return dto
