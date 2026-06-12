from typing import Any

from todo_rpg.application.interfaces.repositories_interfaces import (
    SkillRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol


class ClearExpiredSkillsInteractor:
    def __init__(self, repo: SkillRepositoryProtocol, uow: UoWProtocol) -> None:
        self.repo = repo
        self.uow = uow

    async def __call__(self) -> Any:
        await self.repo.delete_all_skills_deleted_more_than_year()
        await self.uow.commit()
