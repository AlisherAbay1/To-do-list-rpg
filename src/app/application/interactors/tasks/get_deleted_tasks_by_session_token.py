from src.app.application.interfaces.repositories_interfaces import TaskRepositoryProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.exceptions import SessionNotFoundError
from src.app.application.dto.tasks import TaskDTO
from src.app.domain.tasks import TaskRewardCalculatorDomain
from uuid import UUID

class GetDeletedTasksBySessionTokenInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, cash_repo: RedisRepositoryProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, session_token: str):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        tasks = await self.repo.get_deleted_tasks_by_user_id(UUID(user_id))
        tasks_list = []
        for task in tasks:
            rewards = TaskRewardCalculatorDomain(
                task_type=task.type, 
                task_difficulty=task.difficulty, 
                task_priority=task.priority, 
                custom_xp_reward=task.custom_xp_reward, 
                custom_gold_reward=task.custom_gold_reward
            ).calculate_task_rewards()
            dto = TaskDTO(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                category_id=task.category_id,
                xp=rewards.xp,
                gold=rewards.gold,  
                repeat_limit=task.repeat_limit,
                repeat_frequency=task.repeat_frequency, 
                deadline=task.deadline
            )
            tasks_list.append(dto)
        return tasks_list