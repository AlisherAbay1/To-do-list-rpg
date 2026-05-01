from src.app.domain import Skill, Task
from src.app.application.dto import SkillWithTasksDTO
from typing import Sequence
from src.app.application.mappers import TaskMapper

class ExtendedSkillMapper:
    @staticmethod
    def to_with_tasks_dto(domain: Skill, task_domains: Sequence[Task]) -> SkillWithTasksDTO:
        dto = SkillWithTasksDTO(
            id=domain.id,
            user_id=domain.user_id, 
            title=domain.title, 
            description=domain.description, 
            ico=domain.ico, 
            lvl=domain.lvl, 
            xp=domain.xp, 
            deleted=domain.deleted, 
            deleted_at=domain.deleted_at, 
            tasks=TaskMapper.to_list_dto(task_domains)
        )
        return dto