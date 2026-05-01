from src.app.application.interfaces.repositories_interfaces import \
    SkillRepositoryProtocol, TaskRepositoryProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.mappers import ExtendedSkillMapper
from uuid import UUID
from src.app.application.exceptions import SkillNotFoundError, SessionNotFoundError, AccessDeniedError

class GetCurrentUserSkillByIdInteractor:
    def __init__(self, 
                 skill_repo: SkillRepositoryProtocol, 
                 task_repo: TaskRepositoryProtocol,
                 cash_repo: RedisRepositoryProtocol) -> None:
        self.skill_repo = skill_repo
        self.task_repo = task_repo
        self.cash_repo = cash_repo

    async def __call__(self, skill_id: UUID, session_token: str, get_related_tasks: bool):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        skill = await self.skill_repo.get_skill_by_id(skill_id)
        if skill is None:
            raise SkillNotFoundError()
        if skill.user_id != user_id:
            raise AccessDeniedError()
        
        if get_related_tasks:
            tasks = await self.task_repo.get_tasks_by_skill_id(skill_id)
        else: 
            tasks = []
        dto = ExtendedSkillMapper.to_with_tasks_dto(skill, tasks)
        return dto