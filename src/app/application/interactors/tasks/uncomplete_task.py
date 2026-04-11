from src.app.application.interfaces.repositories_interfaces import TaskRepositoryProtocol, TaskHistoryRepositoryProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.exceptions import TaskNotFoundError, SessionNotFoundError, TaskAccessDeniedError
from src.app.application.dto.tasks import TaskDTO
from uuid import UUID

class UncompleteTaskInteractor:
    def __init__(self, task_repo: TaskRepositoryProtocol, task_history_repo: TaskHistoryRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.task_repo = task_repo
        self.task_history_repo = task_history_repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, task_id: UUID, session_token: str):
        task = await self.task_repo.get_task_with_user_and_skills(task_id)
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        tasks_history = await self.task_history_repo.get_recent_history_with_skills(task_id, 2)
        if user_id is None:
            raise SessionNotFoundError()
        if task is None:
            raise TaskNotFoundError()
        if not tasks_history:
            raise TaskNotFoundError()
        if task.user_id != UUID(user_id):
            raise TaskAccessDeniedError()
        if task.repeat_limit is not None:
            task.repeat_limit += 1
        task.last_completed_at = tasks_history[-1].completed_at # previous completion
        task.user.xp -= tasks_history[0].xp_earned
        task.user.lvl = task.user.xp // 1000
        task.user.gold -= tasks_history[0].gold_earned
        for skill in tasks_history[0].skills: 
            skill.xp -= tasks_history[0].xp_earned

        dto = TaskDTO(
            id=UUID(str(task_id)),
            user_id=UUID(str(user_id)),
            title=task.title,
            description=task.description,
            category_id=task.category_id,
            xp=tasks_history[0].xp_earned,
            gold=tasks_history[0].gold_earned,  
            repeat_limit=task.repeat_limit,
            repeat_frequency=task.repeat_frequency, 
            deadline=task.deadline
        )
        
        await self.transaction.delete(tasks_history[0])

        await self.transaction.commit()

        return dto