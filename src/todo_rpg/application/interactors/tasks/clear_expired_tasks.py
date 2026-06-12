from todo_rpg.application.interfaces.repositories_interfaces import (
    TaskRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol


class ClearExpiredTasksInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, uow: UoWProtocol) -> None:
        self.repo = repo
        self.uow = uow

    async def __call__(self) -> None:
        await self.repo.delete_all_tasks_deleted_more_than_year()
        await self.uow.commit()
