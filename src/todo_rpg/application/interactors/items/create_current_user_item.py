from todo_rpg.application.dto.common.items import ItemCreateDTO
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.repositories_interfaces import (
    ItemRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import TransactionProtocol
from todo_rpg.domain import Item
from todo_rpg.application.exceptions import SessionNotFoundError
from todo_rpg.application.mappers.common import ItemMapper


class CreateCurrentUserItemInteractor:
    def __init__(
        self,
        repo: ItemRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        transaction: TransactionProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_token: str, dto: ItemCreateDTO):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        item = Item(user_id=user_id, title=dto.title, description=dto.description)
        output_dto = ItemMapper.to_dto(item)
        await self.transaction.save(item)
        await self.transaction.commit()
        return output_dto
