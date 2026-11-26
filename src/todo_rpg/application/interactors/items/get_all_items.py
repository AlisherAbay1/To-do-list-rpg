from todo_rpg.application.interfaces import (
    ItemRepositoryProtocol,
)
from todo_rpg.application.mappers.common import ItemMapper
from todo_rpg.application.dto import ItemDTO
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    UserNotFoundError,
    AccessDeniedError,
)


class GetAllItemsInteractor:
    def __init__(self, repo: ItemRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(
        self, limit: int, offset: int, session_token: str
    ) -> list[ItemDTO]:
        user_id = await self.session_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.user_repo.get_user(user_id)
        if user is None:
            raise UserNotFoundError()
        if not user.is_admin:
            raise AccessDeniedError()

        items = await self.repo.get_all_items(limit, offset)
        dtos = ItemMapper.to_list_dto(items)
        return dtos
