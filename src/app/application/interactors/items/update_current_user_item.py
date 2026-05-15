from src.app.application.exceptions import SessionNotFoundError
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.repositories_interfaces import (
    ItemRepositoryProtocol,
)
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.mappers.common import ItemMapper
from uuid import UUID
from src.app.application.dto import ItemUpdateDTO
from src.app.application.exceptions import ItemNotFoundError, AccessDeniedError
from src.app.application.dto.sentinel_types import Unset


class UpdateCurrentUserItemInteractor:
    def __init__(
        self,
        repo: ItemRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        transaction: TransactionProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, item_id: UUID, session_token: str, dto: ItemUpdateDTO):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        item = await self.repo.get_item_by_id(item_id)
        if item is None:
            raise ItemNotFoundError()
        if user_id != item.user_id:
            raise AccessDeniedError()

        if not isinstance(dto.title, Unset):
            item.title = dto.title
        if not isinstance(dto.description, Unset):
            item.description = dto.description

        output_dto = ItemMapper.to_dto(item)

        await self.transaction.commit()

        return output_dto
