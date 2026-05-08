from src.app.application.dto.common.items import ItemCreateDTO, ItemDTO
from src.app.application.interfaces.cash_interfaces import \
    RedisRepositoryProtocol
from src.app.application.interfaces.repositories_interfaces import \
    ItemRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import \
    TransactionProtocol
from src.app.domain import ItemRequirement
from src.app.application.exceptions import SessionNotFoundError, ItemNotFoundError
from src.app.application.mappers import ItemExtendedMapper
from uuid import UUID

class AddCurrentUserItemRequirementInteractor:
    def __init__(self, repo: ItemRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, item_id: UUID, skill_id: UUID, requirement_lvl: int, session_token: str):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        item_requirement = ItemRequirement(
            item_id=item_id, 
            skill_id=skill_id, 
            required_lvl=requirement_lvl
        )
        await self.transaction.save(item_requirement)
        await self.transaction.flush()
        item = await self.repo.get_item_by_id_with_requirements_contains_skill(item_id, user_id)
        if item is None:
            raise ItemNotFoundError()
        dto = ItemExtendedMapper.to_dto_with_requirements(item)
        await self.transaction.commit()
        return dto