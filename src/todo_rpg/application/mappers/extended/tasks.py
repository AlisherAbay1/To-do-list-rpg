from typing import Sequence

from todo_rpg.domain import Task, Skill, Item, User
from todo_rpg.application.dto import TaskWithSkillsAndItemsDTO, TaskWithUserAndSkillsDTO
from todo_rpg.application.mappers.common.skills import SkillMapper
from todo_rpg.application.mappers.common.items import ItemMapper
from todo_rpg.application.mappers.common.users import UserMapper


class ExtendedTaskMapper:
    @staticmethod
    def to_dto_with_skills_and_items(
        task_domain: Task, skill_domains: Sequence[Skill], item_domains: Sequence[Item]
    ):
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
            last_completed_at=task_domain.last_completed_at,
            type=task_domain.type,
            difficulty=task_domain.difficulty,
            priority=task_domain.priority,
            custom_xp_reward=task_domain.custom_xp_reward,
            custom_gold_reward=task_domain.custom_gold_reward,
            deleted=task_domain.deleted,
            deleted_at=task_domain.deleted_at,
            skills=SkillMapper.to_list_dto(skill_domains),
            items=ItemMapper.to_list_dto(item_domains),
        )
        return dto

    @staticmethod
    def to_dto_with_skills_and_user(
        task_domain: Task, user_domain: User, skill_domains: Sequence[Skill]
    ):
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
            skills=SkillMapper.to_list_dto(skill_domains),
        )
        return dto
