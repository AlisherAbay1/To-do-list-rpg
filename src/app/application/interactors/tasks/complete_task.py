from src.app.application.interfaces.repositories_interfaces import TaskRepositoryProtocol, TaskHistoryRepositoryProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.dto_mappers import TaskDtoMapper
from src.app.application.exceptions import TaskNotFoundError, SessionNotFoundError, TaskAccessDeniedError
from uuid import UUID

class CompleteTaskInteractor:
    def __init__(self, 
                 task_repo: TaskRepositoryProtocol, 
                 task_history_repo: TaskHistoryRepositoryProtocol,
                 cash_repo: RedisRepositoryProtocol, 
                 transaction: TransactionProtocol) -> None:
        self.task_repo = task_repo
        self.task_history_repo = task_history_repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, task_id: UUID, session_token: str):
        task = await self.task_repo.get_task_with_user_and_skills(task_id)
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        if task is None:
            raise TaskNotFoundError()
        if task.user_id != UUID(user_id):
            raise TaskAccessDeniedError()

        task.complete()
        rewards = task.calculate_task_rewards()

        for skill in task.skills:
            skill.add_xp(rewards.xp)
        task.user.add_xp(rewards.xp)
        task.user.add_gold(rewards.gold)
        
        await self.task_repo.save_completion(task)
        await self.task_history_repo.save_completion(task, rewards)

        dto = TaskDtoMapper.to_dto(task, rewards)
        
        await self.transaction.commit()
        return dto