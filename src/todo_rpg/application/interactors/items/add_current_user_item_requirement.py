from todo_rpg.application.interfaces import (
    ItemRepositoryProtocol,
    SkillRepositoryProtocol,
    RedisRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol
from todo_rpg.domain import ItemRequirement
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    ItemNotFoundError,
    AccessDeniedError,
)
from todo_rpg.domain.exceptions import SkillIsAlreadyInRequirementsError
from todo_rpg.application.mappers import ItemExtendedMapper
from uuid import UUID
from todo_rpg.application.dto import ItemWithRequirementsDTO


class AddCurrentUserItemRequirementInteractor:
    def __init__(
        self,
        item_repo: ItemRepositoryProtocol,
        skill_repo: SkillRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.item_repo = item_repo
        self.skill_repo = skill_repo
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(
        self, item_id: UUID, skill_id: UUID, requirement_lvl: int, session_token: str
    ) -> ItemWithRequirementsDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()

        item = await self.item_repo.get_item_by_id(item_id)
        if item is None:
            raise ItemNotFoundError()
        if item.user_id != user_id:
            raise AccessDeniedError()
        if skill_id in [reqirement.skill_id for reqirement in item.requirements]:
            raise SkillIsAlreadyInRequirementsError()
        item_requirement = ItemRequirement(
            item_id=item_id, skill_id=skill_id, required_lvl=requirement_lvl
        )

        item.requirements.append(item_requirement)
        await self.uow.flush()

        item = await self.item_repo.get_item_by_id(item_id)
        if item is None:
            raise ItemNotFoundError()

        dto = ItemExtendedMapper.to_dto_with_requirements(item)

        await self.uow.commit()
        return dto
