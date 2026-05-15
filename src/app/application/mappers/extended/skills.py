from src.app.domain import Skill, Task
from src.app.application.dto import SkillWithTasksAndNextLvlXpDTO
from typing import Sequence
from src.app.application.mappers import TaskMapper


class ExtendedSkillMapper:
    @staticmethod
    def to_with_tasks_and_next_lvl_xp_dto(
        domain: Skill, task_domains: Sequence[Task]
    ) -> SkillWithTasksAndNextLvlXpDTO:
        dto = SkillWithTasksAndNextLvlXpDTO(
            id=domain.id,
            user_id=domain.user_id,
            title=domain.title,
            description=domain.description,
            ico=domain.ico,
            lvl=domain.lvl,
            xp=domain.xp,
            deleted=domain.deleted,
            deleted_at=domain.deleted_at,
            xp_for_next_lvl=domain.calculate_xp_for_next_lvl(domain.xp),
            tasks=TaskMapper.to_list_dto(task_domains),
        )
        return dto
