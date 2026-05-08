from uuid import UUID

from src.app.application.mappers import ExtendedTaskMapper
from src.app.application.exceptions import TaskNotFoundError, SessionNotFoundError
from src.app.application.interfaces.repositories_interfaces import (
    ItemRepositoryProtocol, SkillRepositoryProtocol, TaskRepositoryProtocol)
from src.app.application.interfaces.cash_interfaces import \
    RedisRepositoryProtocol

class GetCurrentUserTaskInteractor:
    def __init__(self, 
                 task_repo: TaskRepositoryProtocol,
                 skill_repo: SkillRepositoryProtocol, 
                 item_repo: ItemRepositoryProtocol, 
                 cash_repo: RedisRepositoryProtocol) -> None:
        self.task_repo = task_repo
        self.skill_repo = skill_repo
        self.item_repo = item_repo
        self.cash_repo = cash_repo

    async def __call__(self, session_token: str, task_id: UUID, get_related_skills: bool, get_related_items: bool):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        task = await self.task_repo.get_task_by_id(task_id, user_id)
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
        
