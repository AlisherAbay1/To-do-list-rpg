from typing import Sequence

from src.app.domain import Task, Skill, Item, User
from src.app.application.dto.tasks import (TaskDTO, TaskWithSkillsAndItemsDTO, TaskWithUserAndSkillsDTO, 
                                           TaskDetailDTO)
from src.app.application.dto_mappers.skills import SkillMapper 
from src.app.application.dto_mappers.items import ItemMapper
from src.app.application.dto_mappers.users import UserMapper

class TaskMapper:
    @staticmethod
    def to_dto(domain: Task) -> TaskDTO:
        rewards = domain.calculate_task_rewards()
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
    def to_list_dto(domains: Sequence[Task]) -> list[TaskDTO]:
        return [TaskMapper.to_dto(domain) for domain in domains]

    @staticmethod
    def to_detail_dto(domain: Task) -> TaskDetailDTO:
        dto = TaskDetailDTO(
            id=domain.id,
            user_id=domain.user_id,
            title=domain.title, 
            description=domain.description, 
            category_id=domain.category_id,
            repeat_limit=domain.repeat_limit,
            repeat_frequency=domain.repeat_frequency,
            deadline=domain.deadline,
            last_completed_at=domain.last_completed_at,
            created_at=domain.created_at,
            type=domain.type,
            difficulty=domain.difficulty,
            priority=domain.priority,
            custom_xp_reward=domain.custom_xp_reward,
            custom_gold_reward=domain.custom_gold_reward, 
            deleted=domain.deleted,
            deleted_at=domain.deleted_at
        )
        return dto
    
    @staticmethod
    def to_list_detail_dto(domains: Sequence[Task]) -> list[TaskDetailDTO]:
        return [TaskMapper.to_detail_dto(domain) for domain in domains]

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
            skills=SkillMapper.to_list_dto(skill_domains),  
            items=ItemMapper.to_list_dto(item_domains)
        )
        return dto
    
    @staticmethod
    def to_dto_with_skills_and_user(task_domain: Task, 
                                    user_domain: User,
                                    skill_domains: Sequence[Skill]):
        rewards = task_domain.calculate_task_rewards()
        dto = TaskWithUserAndSkillsDTO(
            id=task_domain.id,
            title=task_domain.title,
            description=task_domain.description,
            category_id=task_domain.category_id,
            xp=rewards.xp,
            gold=rewards.gold,
            repeat_limit=task_domain.repeat_limit,
            repeat_frequency=task_domain.repeat_frequency,
            deadline=task_domain.deadline,
            user=UserMapper.to_dto(user_domain),
            skills=SkillMapper.to_list_dto(skill_domains)
        )
        return dto