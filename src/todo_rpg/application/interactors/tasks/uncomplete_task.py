from uuid import UUID

from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    TaskNotFoundError,
    UserNotFoundError,
)
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.repositories_interfaces import (
    SkillRepositoryProtocol,
    TaskHistoryRepositoryProtocol,
    TaskRepositoryProtocol,
    UserRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol
from todo_rpg.application.mappers import ExtendedTaskMapper


class UncompleteTaskInteractor:
    def __init__(
        self,
        task_repo: TaskRepositoryProtocol,
        user_repo: UserRepositoryProtocol,
        skill_repo: SkillRepositoryProtocol,
        task_history_repo: TaskHistoryRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.task_repo = task_repo
        self.user_repo = user_repo
        self.skill_repo = skill_repo
        self.task_history_repo = task_history_repo
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(self, task_id: UUID, session_token: str):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        tasks_history = await self.task_history_repo.get_recent_history_with_skills(
            task_id, 2
        )
        if user_id is None:
            raise SessionNotFoundError()
        task = await self.task_repo.get_task_by_id(task_id, user_id)
        if task is None:
            raise TaskNotFoundError()
        if not tasks_history:
            raise TaskNotFoundError()
        if task.repeat_limit is not None:
            task.repeat_limit += 1

        before_previous, previous = tasks_history[-1], tasks_history[0]
        user = await self.user_repo.get_user(user_id)
        skills = await self.skill_repo.get_skills_by_task_id(task_id)

        if user is None:
            raise UserNotFoundError()

        if len(tasks_history) < 2:
            task.last_completed_at = None
        else:
            task.last_completed_at = before_previous.completed_at
        user.xp -= previous.xp_earned
        user.lvl = 1 + user.xp // 1000
        user.gold -= previous.gold_earned
        for skill in previous.skills:
            skill.xp -= previous.xp_earned

        dto = ExtendedTaskMapper.to_dto_with_skills_and_user(task, user, skills)

        await self.uow.delete(tasks_history[0])

        await self.uow.commit()

        return dto
