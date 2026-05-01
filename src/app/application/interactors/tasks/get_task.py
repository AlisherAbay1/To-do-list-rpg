from uuid import UUID

from src.app.application.mappers import ExtendedTaskMapper
from src.app.application.exceptions import TaskNotFoundError
from src.app.application.interfaces.repositories_interfaces import (
    ItemRepositoryProtocol, SkillRepositoryProtocol, TaskRepositoryProtocol)


class GetTaskInteractor:
    def __init__(self, 
                 task_repo: TaskRepositoryProtocol,
                 skill_repo: SkillRepositoryProtocol, 
                 item_repo: ItemRepositoryProtocol) -> None:
        self.task_repo = task_repo
        self.skill_repo = skill_repo
        self.item_repo = item_repo

    async def __call__(self, task_id: UUID, get_related_skills: bool, get_related_items: bool):
        task = await self.task_repo.get_task_by_id(task_id)
        if task is None:
            raise TaskNotFoundError()
        if get_related_skills:
            skills = await self.skill_repo.get_skills_by_task_id(task_id)
        else: 
            skills = []
        if get_related_items:
            items = await self.item_repo.get_items_by_task_id(task_id)
        else:
            items = []

        return ExtendedTaskMapper.to_dto_with_skills_and_items(task, skills, items)
        
