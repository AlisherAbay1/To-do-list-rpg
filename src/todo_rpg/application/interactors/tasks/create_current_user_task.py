from uuid6 import uuid7

from todo_rpg.application.dto import TaskCreateDTO
from todo_rpg.application.exceptions import SessionNotFoundError
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.repositories_interfaces import (
    TaskRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import TransactionProtocol
from todo_rpg.domain import Task
from todo_rpg.infrastructure.database.models import Tasks_to_items, Tasks_to_skills
from todo_rpg.application.mappers.common import TaskMapper


class CreateCurrentUserTaskInteractor:
    def __init__(
        self,
        repo: TaskRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        transaction: TransactionProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_token, dto: TaskCreateDTO):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        task_id = uuid7()
        task = Task(
            user_id=user_id,
            title=dto.title,
            description=dto.description,
            category_id=dto.category_id,
            repeat_limit=dto.repeat_limit,
            repeat_frequency=dto.repeat_frequency,
            deadline=dto.deadline,
            type=dto.type,
            difficulty=dto.difficulty,
            priority=dto.priority,
            custom_xp_reward=dto.custom_xp_reward,
            custom_gold_reward=dto.custom_gold_reward,
        )

        await self.transaction.save(task)
        await self.transaction.flush()

        for skill_id in dto.related_skills:
            skill_relationship = Tasks_to_skills(task_id=task_id, skill_id=skill_id)
            await self.transaction.save(skill_relationship)

        for item_id in dto.related_items:
            item_relationship = Tasks_to_items(task_id=task_id, item_id=item_id)
            await self.transaction.save(item_relationship)

        output_dto = TaskMapper.to_dto(task)

        await self.transaction.commit()

        return output_dto
