from src.app.application.interfaces.repositories_interfaces import TaskRepositoryProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.exceptions import SessionNotFoundError
from src.app.application.dto.tasks import TaskDryDTO
from uuid import UUID

class GetCurentUserTasksInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, cash_repo: RedisRepositoryProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, session_token, limit: int, offset: int):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        tasks = await self.repo.get_tasks_by_user_id(UUID(user_id), limit, offset)
        return [TaskDryDTO(
            id=task.id,
            user_id=task.user_id,
            title=task.title, 
            description=task.description, 
            category_id=task.category_id,
            repeat_limit=task.repeat_limit,
            repeat_frequency=task.repeat_frequency,
            deadline=task.deadline,
            last_completed_at=task.last_completed_at,
            created_at=task.created_at,
            type=task.type,
            difficulty=task.difficulty,
            priority=task.priority,
            custom_xp_reward=task.custom_xp_reward,
            custom_gold_reward=task.custom_gold_reward
            ) for task in tasks]