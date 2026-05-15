from datetime import datetime, timezone

from src.app.application.exceptions import (
    SkillNotFoundError,
    SessionNotFoundError,
    AccessDeniedError,
)
from src.app.application.interfaces.repositories_interfaces import (
    SkillRepositoryProtocol,
)
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from uuid import UUID


class DeleteCurrentUserSkillByIdInteractor:
    def __init__(
        self,
        repo: SkillRepositoryProtocol,
        transaction: TransactionProtocol,
        cash_repo: RedisRepositoryProtocol,
    ) -> None:
        self.repo = repo
        self.transaction = transaction
        self.cash_repo = cash_repo

    async def __call__(self, skill_id: UUID, session_token: str):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        skill = await self.repo.get_skill_by_id(skill_id)
        if skill is None:
            raise SkillNotFoundError()
        if skill.user_id != user_id:
            raise AccessDeniedError()
        skill.deleted = True
        skill.deleted_at = datetime.now(tz=timezone.utc)
        await self.transaction.commit()
