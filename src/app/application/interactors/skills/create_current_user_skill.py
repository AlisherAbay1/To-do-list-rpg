from uuid import UUID

from uuid6 import uuid7

from src.app.application.dto.common.skills import SkillCreateDTO, SkillDTO
from src.app.application.interfaces.cash_interfaces import \
    RedisRepositoryProtocol
from src.app.application.interfaces.repositories_interfaces import \
    SkillRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import \
    TransactionProtocol
from src.app.domain import Skill
from src.app.application.exceptions import SessionNotFoundError
from src.app.application.mappers.common import SkillMapper

class CreateCurrentUserSkillInteractor:
    def __init__(self, repo: SkillRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_token: str, dto: SkillCreateDTO):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        skill = Skill(
            user_id=user_id, 
            title=dto.title, 
            description=dto.description, 
            ico=dto.ico, 
            lvl=dto.lvl, 
            xp=dto.xp
        )
        output_dto = SkillMapper.to_dto(skill)
        await self.transaction.save(skill)
        await self.transaction.commit()
        return output_dto