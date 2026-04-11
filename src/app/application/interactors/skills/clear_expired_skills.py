from typing import Any
from src.app.application.interfaces.repositories_interfaces import SkillRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol

class ClearExpiredSkillsInteractor:
    def __init__(self, repo: SkillRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.transaction = transaction

    async def __call__(self) -> Any:
        await self.repo.delete_all_skills_deleted_more_than_year()
        await self.transaction.commit()