from src.app.infrastructure.database.models.tasks import Task
from src.app.domain import TaskDomain

class TaskMapper:
    @staticmethod
    def to_domain(orm: Task):
        task = TaskDomain(
            id=orm.id,
            user_id=orm.user_id,
            title=orm.title,
            description=orm.description,
            category_id=orm.category_id,
            repeat_limit=orm.repeat_limit,
            repeat_frequency=orm.repeat_frequency,
            deadline=orm.deadline,
            last_completed_at=orm.last_completed_at,
            created_at=orm.created_at,
            type=orm.type,
            difficulty=orm.difficulty,
            priority=orm.priority,
            custom_xp_reward=orm.custom_xp_reward,
            custom_gold_reward=orm.custom_gold_reward
        )
        return task
    
    @staticmethod
    def update_orm(domain: TaskDomain, orm: Task) -> None:
        orm.id = domain.id
        orm.user_id = domain.user_id
        orm.title = domain.title
        orm.description = domain.description
        orm.category_id = domain.category_id
        orm.repeat_limit = domain.repeat_limit
        orm.repeat_frequency = domain.repeat_frequency
        orm.deadline = domain.deadline
        orm.last_completed_at = domain.last_completed_at
        orm.created_at = domain.created_at
        orm.type = domain.type
        orm.difficulty = domain.difficulty
        orm.priority = domain.priority
        orm.custom_xp_reward = domain.custom_xp_reward
        orm.custom_gold_reward = domain.custom_gold_reward