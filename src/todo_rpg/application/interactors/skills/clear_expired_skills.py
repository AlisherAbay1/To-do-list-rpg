from todo_rpg.application.interfaces import SkillRepositoryProtocol, UoWProtocol


class ClearExpiredSkillsInteractor:
    def __init__(self, repo: SkillRepositoryProtocol, uow: UoWProtocol) -> None:
        self.repo = repo
        self.uow = uow

    async def __call__(self) -> None:
        await self.repo.delete_all_skills_deleted_more_than_year()
        await self.uow.commit()
