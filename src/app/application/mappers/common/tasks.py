from typing import Sequence

from src.app.domain import Task
from src.app.application.dto import TaskDTO, TaskDetailDTO

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