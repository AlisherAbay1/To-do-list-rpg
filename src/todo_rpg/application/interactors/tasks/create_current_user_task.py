from todo_rpg.application.dto import TaskCreateDTO
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    TaskCategoryNotFoundError,
)
from todo_rpg.application.interfaces import (
    RedisRepositoryProtocol,
    TaskRepositoryProtocol,
    SkillRepositoryProtocol,
    ItemRepositoryProtocol,
    TaskCategoriesRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol
from todo_rpg.domain import Task
from todo_rpg.application.mappers.common import TaskMapper
from todo_rpg.application.dto import TaskDTO


class CreateCurrentUserTaskInteractor:
    def __init__(
        self,
        task_repo: TaskRepositoryProtocol,
        task_category_repo: TaskCategoriesRepositoryProtocol,
        skill_repo: SkillRepositoryProtocol,
        item_repo: ItemRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.task_repo = task_repo
        self.task_category_repo = task_category_repo
        self.skill_repo = skill_repo
        self.item_repo = item_repo
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(self, session_token, dto: TaskCreateDTO) -> TaskDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        if dto.category_id is not None:
            task_category = await self.task_category_repo.get_task_category_by_id(
                dto.category_id
            )
            if task_category is None:
                raise TaskCategoryNotFoundError()

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

        skills = await self.skill_repo.get_skills_by_ids(dto.related_skills)
        items = await self.item_repo.get_items_by_ids(dto.related_items)

        task.skills = list(skills)
        task.items = list(items)

        output_dto = TaskMapper.to_dto(task)

        await self.uow.add(task)
        await self.uow.commit()

        return output_dto
