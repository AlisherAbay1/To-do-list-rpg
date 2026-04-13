from src.app.domain import TaskDomain
from src.app.application.dto.tasks import TaskDTO, TaskReward

class TaskDtoMapper:
    @staticmethod
    def to_dto(domain: TaskDomain, rewards: TaskReward):
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