from todo_rpg.application.exceptions import SessionNotFoundError
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.repositories_interfaces import (
    ItemRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol
from todo_rpg.application.mappers.common import ItemMapper
from uuid import UUID
from todo_rpg.application.dto import ItemUpdateDTO
from todo_rpg.application.exceptions import ItemNotFoundError, AccessDeniedError
from todo_rpg.application.dto.sentinel_types import Unset
from todo_rpg.application.dto import ItemDTO


class UpdateCurrentUserItemInteractor:
    def __init__(
        self,
        repo: ItemRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(
        self, item_id: UUID, session_token: str, dto: ItemUpdateDTO
    ) -> ItemDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        item = await self.repo.get_item_by_id(item_id)
        if item is None:
            raise ItemNotFoundError()
        if item.user_id != user_id:
            raise AccessDeniedError()

        if not isinstance(dto.title, Unset) and dto.title is not None:
            item.title = dto.title
        if not isinstance(dto.description, Unset):
            item.description = dto.description

        output_dto = ItemMapper.to_dto(item)

        await self.uow.commit()

        return output_dto
