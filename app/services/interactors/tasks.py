from app.repositories.interfaces import TaskRepositoryProtocol, RedisRepositoryProtocol, TransactionProtocol, \
                                        TaskHistoryRepositoryProtocol
from app.exceptions import TaskNotFoundError, TaskAlreadyDoneError, SessionNotFoundError, \
                           TaskAccessDeniedError, TaskExecutedTooEarlyError
from app.schemas.dto import TaskCreateDTO, TaskDTO, TaskFilterParamsDTO, \
                            TaskSortParamsDTO, TaskWithSkillsAndItemsDTO, SkillDTO, \
                            ItemDTO, TaskUpdateDTO, TaskDryDTO
from app.domain import TaskRewardCalculatorDomain
from app.schemas.sentinel_types import Unset
from app.enums import TaskRepeatFrequency
from app.models import Task, Tasks_to_skills, Tasks_to_items, TaskHistory, Tasks_history_to_skills
from uuid import UUID
from uuid_utils import uuid7
from datetime import datetime, timezone, timedelta

class GetAllTasksInteractor:
    def __init__(self, repo: TaskRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, filters: TaskFilterParamsDTO, sorting: TaskSortParamsDTO, limit: int, offset: int):
        tasks = await self.repo.get_all_tasks(filters, sorting, limit, offset)
        return list(tasks)

class CreateCurrentUserTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_token, dto: TaskCreateDTO):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        task_id=uuid7()
        task = Task(
            id=task_id,
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
            custom_gold_reward=dto.custom_gold_reward
        )

        await self.transaction.save(task)
        await self.transaction.flush()

        for skill_id in dto.related_skills:
            relationship = Tasks_to_skills(
                task_id=task_id,
                skill_id=skill_id
            )
            await self.transaction.save(relationship)
        
        for item_id in dto.related_items:
            relationship = Tasks_to_items(
                task_id=task_id,
                item_id=item_id
            )
            await self.transaction.save(relationship)

        await self.transaction.commit()

        rewards = TaskRewardCalculatorDomain(
            task_type=dto.type, 
            task_difficulty=dto.difficulty, 
            task_priority=dto.priority, 
            custom_xp_reward=dto.custom_xp_reward, 
            custom_gold_reward=dto.custom_gold_reward
        ).calculate_task_rewards()

        return TaskDTO(
            id=UUID(str(task_id)),
            user_id=UUID(str(user_id)),
            title=dto.title,
            description=dto.description,
            category_id=dto.category_id,
            xp=rewards.xp,
            gold=rewards.gold,  
            repeat_limit=dto.repeat_limit,
            repeat_frequency=dto.repeat_frequency, 
            deadline=dto.deadline
        )

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

class GetTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, task_id: UUID, get_related_skills: bool, get_related_items: bool):
        task = await self.repo.get_task_by_id(task_id, get_related_skills, get_related_items)
        if task is None:
            raise TaskNotFoundError()
        return TaskWithSkillsAndItemsDTO(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                category_id=task.category_id,
                repeat_limit=task.repeat_limit,
                repeat_frequency=task.repeat_frequency, 
                deadline=task.deadline, 
                created_at=task.created_at,
                type=task.type,
                difficulty=task.difficulty, 
                priority=task.priority,
                custom_xp_reward=task.custom_xp_reward,
                custom_gold_reward=task.custom_gold_reward,
                skills=[SkillDTO(
                        id=skill.id,
                        user_id=skill.user_id, 
                        title=skill.title, 
                        description=skill.description, 
                        ico=skill.ico, 
                        lvl=skill.lvl, 
                        xp=skill.xp, 
                        deleted=skill.deleted, 
                        deleted_at=skill.deleted_at)
                            for skill in task.skills],  
                items=[ItemDTO(
                        id=item.id,
                        user_id=item.user_id, 
                        title=item.title, 
                        description=item.description, 
                        deleted=item.deleted, 
                        deleted_at=item.deleted_at) 
                            for item in task.items]
            )

class CompleteTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, task_id: UUID, session_token: str):
        task = await self.repo.get_task_with_user_and_skills(task_id)
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        current_time = datetime.now(timezone.utc)
        if user_id is None:
            raise SessionNotFoundError()
        if task is None:
            raise TaskNotFoundError()
        if task.user_id != UUID(user_id):
            raise TaskAccessDeniedError()
        if task.repeat_limit is not None:
            if task.repeat_limit == 0:
                raise TaskAlreadyDoneError()
            if task.repeat_limit > 0:
                task.repeat_limit -= 1
        if task.last_completed_at != None:
            match task.repeat_frequency:
                case TaskRepeatFrequency.DAILY:
                    if current_time < task.last_completed_at + timedelta(days=1):
                        raise TaskExecutedTooEarlyError()
                case TaskRepeatFrequency.ONCE_TWO_DAYS:
                    if current_time < task.last_completed_at + timedelta(days=2):
                        raise TaskExecutedTooEarlyError()
                case TaskRepeatFrequency.WEEKLY:
                    if current_time < task.last_completed_at + timedelta(days=7):
                        raise TaskExecutedTooEarlyError()
        task.last_completed_at = current_time
        rewards = TaskRewardCalculatorDomain(
            task_type=task.type, 
            task_difficulty=task.difficulty, 
            task_priority=task.priority, 
            custom_xp_reward=task.custom_xp_reward, 
            custom_gold_reward=task.custom_gold_reward
        ).calculate_task_rewards()

        skills = task.skills
        for skill in skills:
            skill.xp += rewards.xp
            skill.lvl = skill.lvl // 1000
        print(task.user.xp)
        task.user.xp = task.user.xp + rewards.xp
        task.user.gold += rewards.gold
        task.user.lvl = task.user.xp // 1000
        
        dto = TaskDTO(
            id=UUID(str(task_id)),
            user_id=UUID(str(user_id)),
            title=task.title,
            description=task.description,
            category_id=task.category_id,
            xp=rewards.xp,
            gold=rewards.gold,  
            repeat_limit=task.repeat_limit,
            repeat_frequency=task.repeat_frequency, 
            deadline=task.deadline
        )
        task_history_id = uuid7()
        task_history = TaskHistory(
            id=task_history_id, 
            user_id=task.user_id,
            task_id=task.id, 
            title=task.title, 
            completed_at=current_time, 
            xp_earned=rewards.xp, 
            gold_earned=rewards.gold
        )
        await self.transaction.save(task_history)
        await self.transaction.flush()

        for skill in skills:
            skill_history = Tasks_history_to_skills(
                task_history_id=task_history_id, 
                skill_id=skill.id
            )
            await self.transaction.save(skill_history)

        await self.transaction.commit()
        return dto

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

class DeleteTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.transaction = transaction

    async def __call__(self, task_id: UUID):
        task = await self.repo.get_task_by_id(task_id, get_related_skills=False, get_related_items=False)
        if task is None:
            raise TaskNotFoundError()
        task.deleted = True
        task.deleted_at = datetime.now(tz=timezone.utc)
        await self.transaction.delete(task)
        await self.transaction.commit()

class UpdateTaskInteractor:
    def __init__(self, repo: TaskRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, task_id: UUID, dto: TaskUpdateDTO, session_token: str):
        task = await self.repo.get_task_by_id(task_id, False, False)
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if task is None:
            raise TaskNotFoundError()
        if task.user_id != UUID(user_id):
            raise TaskAccessDeniedError()
        
        if not isinstance(dto.title, Unset):
            task.title = dto.title
        if not isinstance(dto.description, Unset):
            task.description = dto.description
        if not isinstance(dto.category_id, Unset):
            task.category_id = dto.category_id
        if not isinstance(dto.repeat_limit, Unset):
            task.repeat_limit = dto.repeat_limit
        if not isinstance(dto.repeat_frequency, Unset):
            task.repeat_frequency = dto.repeat_frequency
        if not isinstance(dto.deadline, Unset):
            task.deadline = dto.deadline
        if not isinstance(dto.type, Unset):
            task.type = dto.type
        if not isinstance(dto.difficulty, Unset):
            task.difficulty = dto.difficulty
        if not isinstance(dto.priority, Unset):
            task.priority = dto.priority
        if not isinstance(dto.custom_xp_reward, Unset):
            task.custom_xp_reward = dto.custom_xp_reward
        if not isinstance(dto.custom_gold_reward, Unset):
            task.custom_gold_reward = dto.custom_gold_reward
        if not isinstance(dto.deleted, Unset):
            task.deleted = dto.deleted

        rewards = TaskRewardCalculatorDomain(
            task_type=task.type, 
            task_difficulty=task.difficulty, 
            task_priority=task.priority, 
            custom_xp_reward=task.custom_xp_reward, 
            custom_gold_reward=task.custom_gold_reward
        ).calculate_task_rewards()
        
        new_dto = TaskDTO(
                    id=task.id,
                    user_id=task.user_id,
                    title=task.title,
                    description=task.description,
                    category_id=task.category_id,
                    xp=rewards.xp,
                    gold=rewards.gold,
                    repeat_limit=task.repeat_limit,
                    repeat_frequency=task.repeat_frequency,
                    deadline=task.deadline,
                )
        await self.transaction.commit()
        return new_dto