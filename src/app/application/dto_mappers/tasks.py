from typing import Sequence

from src.app.domain import Task, Skill, Item
from src.app.application.dto.tasks import TaskDTO, TaskReward, TaskWithSkillsAndItemsDTO
from src.app.application.dto.skills import SkillDTO
from src.app.application.dto.items import ItemDTO

class TaskDtoMapper:
    @staticmethod
    def to_dto(domain: Task, rewards: TaskReward):
        dto = TaskDTO(
            id=domain.id,
            user_id=domain.user_id,
            title=domain.title,
            description=domain.description,
            category_id=domain.category_id,
            xp=rewards.xp,
            gold=rewards.gold,
            repeat_limit=domain.repeat_limit,
            repeat_frequency=domain.repeat_frequency,
            deadline=domain.deadline,
        )
        return dto

    @staticmethod
    def to_dto_with_skills_and_items(task_domain: Task, 
                                     skill_domains: Sequence[Skill], 
                                     item_domains: Sequence[Item]):
        dto = TaskWithSkillsAndItemsDTO(
                id=task_domain.id,
                user_id=task_domain.user_id,
                title=task_domain.title,
                description=task_domain.description,
                category_id=task_domain.category_id,
                repeat_limit=task_domain.repeat_limit,
                repeat_frequency=task_domain.repeat_frequency, 
                deadline=task_domain.deadline, 
                created_at=task_domain.created_at,
                type=task_domain.type,
                difficulty=task_domain.difficulty, 
                priority=task_domain.priority,
                custom_xp_reward=task_domain.custom_xp_reward,
                custom_gold_reward=task_domain.custom_gold_reward,
                skills=[SkillDTO(
                        id=skill.id,
                        user_id=skill.user_id, 
                        title=skill.title, 
                        description=skill.description, 
                        ico=skill.ico, 
                        lvl=skill.lvl, 
                        xp=skill.xp, 
                        deleted=skill.deleted, 
                        deleted_at=skill.deleted_at)
                            for skill in skill_domains],  
                items=[ItemDTO(
                        id=item.id,
                        user_id=item.user_id, 
                        title=item.title, 
                        description=item.description, 
                        deleted=item.deleted, 
                        deleted_at=item.deleted_at) 
                            for item in item_domains]
            )
        return dto