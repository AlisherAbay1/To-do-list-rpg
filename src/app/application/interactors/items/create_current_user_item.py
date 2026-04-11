from src.app.application.interfaces.repositories_interfaces import ItemRepositoryProtocol 
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.dto.items import ItemCreateDTO, ItemDTO
from src.app.infrastructure.database.models import Item
from uuid import UUID
from uuid_utils import uuid7

class CreateCurrentUserItemInteractor:
    def __init__(self, repo: ItemRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_token: str, dto: ItemCreateDTO):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        item_id = uuid7()
        user = Item(
            id=item_id,
            user_id=user_id, 
            title=dto.title, 
            description=dto.description
        )
        await self.transaction.save(user)
        await self.transaction.commit()
        return ItemDTO(
            id=UUID(str(item_id)),
            user_id=UUID(user_id), 
            title=dto.title, 
            description=dto.description
        )