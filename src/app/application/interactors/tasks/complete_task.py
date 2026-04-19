from src.app.application.interfaces.repositories_interfaces import TaskRepositoryProtocol, TaskHistoryRepositoryProtocol, UserRepositoryProtocol, \
                                                                    SkillRepositoryProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.dto_mappers import CompleteTaskDtoMapper
from src.app.application.exceptions import TaskNotFoundError, SessionNotFoundError, TaskAccessDeniedError, \
                                            UserNotFoundError
from uuid import UUID

class CompleteTaskInteractor:
    def __init__(self, 
                 task_repo: TaskRepositoryProtocol, 
                 user_repo: UserRepositoryProtocol, 
                 skill_repo: SkillRepositoryProtocol,
                 task_history_repo: TaskHistoryRepositoryProtocol,
                 cash_repo: RedisRepositoryProtocol, 
                 transaction: TransactionProtocol) -> None:
        self.task_repo = task_repo
        self.user_repo = user_repo
        self.skill_repo = skill_repo
        self.task_history_repo = task_history_repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, task_id: UUID, session_token: str):
        task = await self.task_repo.get_task_by_id(task_id)
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        if task is None:
            raise TaskNotFoundError()
        if task.user_id != UUID(user_id):
            raise TaskAccessDeniedError()
        
        user = await self.user_repo.get_user(UUID(user_id))
        skills = await self.skill_repo.get_skills_by_task_id(task_id)

        if user is None:
            raise UserNotFoundError()
        
        task.complete()
        rewards = task.calculate_task_rewards()

        for skill in skills:
            skill.apply_reward(rewards.xp)
            await self.skill_repo.update(skill)
        user.apply_rewards(rewards)
        
        await self.user_repo.update(user)
        await self.task_repo.update(task)
        await self.task_history_repo.save_completion(task, skills, rewards)

        dto = CompleteTaskDtoMapper.to_dto(task, user, skills, rewards)
        
        await self.transaction.commit()
        return dto