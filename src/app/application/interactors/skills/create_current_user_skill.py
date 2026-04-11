from src.app.application.interfaces.repositories_interfaces import SkillRepositoryProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.dto.skills import SkillCreateDTO, SkillDTO
from src.app.infrastructure.database.models import Skill
from uuid import UUID
from uuid_utils import uuid7

class CreateCurrentUserSkillInteractor:
    def __init__(self, repo: SkillRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_token: str, dto: SkillCreateDTO):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        skill_id = uuid7()
        user = Skill(
            id=skill_id,
            user_id=user_id, 
            title=dto.title, 
            description=dto.description, 
            ico=dto.ico, 
            lvl=dto.lvl, 
            xp=dto.xp
        )
        await self.transaction.save(user)
        await self.transaction.commit()
        return SkillDTO(
            id=UUID(str(skill_id)),
            user_id=UUID(user_id), 
            title=dto.title, 
            description=dto.description, 
            ico=dto.ico, 
            lvl=dto.lvl, 
            xp=dto.xp
        ) 