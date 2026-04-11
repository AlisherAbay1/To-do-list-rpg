from src.app.application.interfaces.repositories_interfaces import SkillRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.exceptions import SkillNotFoundError
from datetime import datetime, timezone

class DeleteSkillInteractor:
    def __init__(self, repo: SkillRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.transaction = transaction

    async def __call__(self, skill_id):
        skill = await self.repo.get_skill_by_id(skill_id)
        if skill is None:
            raise SkillNotFoundError()
        skill.deleted = True
        skill.deleted_at = datetime.now(tz=timezone.utc)
        await self.transaction.commit()
