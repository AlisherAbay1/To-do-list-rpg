from src.app.domain.enums import TaskType, TaskDifficulty, TaskPriority
from src.app.application.dto.tasks import TaskReward
from src.app.domain.enums import TaskRepeatFrequency
from src.app.application.exceptions import TaskAlreadyDoneError, TaskExecutedTooEarlyError
from uuid import UUID
from datetime import datetime, timezone, timedelta
from typing import Optional
from dataclasses import dataclass, field
from uuid6 import uuid7
from src.app.domain.users import UserDomain
from src.app.domain.skills import SkillDomain
from src.app.domain.items import ItemDomain

@dataclass(kw_only=True)
class TaskDomain:
    id: UUID = field(default_factory=uuid7)
    user_id: UUID
    title: str
    description: Optional[str] = None
    category_id: Optional[UUID] = None
    repeat_limit: Optional[int] = None
    repeat_frequency: Optional[TaskRepeatFrequency] = None
    deadline: Optional[datetime] = None
    last_completed_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
    type: Optional[TaskType] = TaskType.AUTO
    difficulty: Optional[TaskDifficulty]
    priority: Optional[TaskPriority]
    custom_xp_reward: Optional[int]
    custom_gold_reward: Optional[int]
    deleted: bool = False
    deleted_at: Optional[datetime] = None

    user: Optional[UserDomain] = field(init=False, default=None)
    skills: list[SkillDomain] = field(init=False, default_factory=list)
    items: list[ItemDomain] = field(init=False, default_factory=list)

    difficulty_multiplier: int = field(init=False, default=0)
    priority_multiplier: int = field(init=False, default=0)

    def complete(self):
        current_time = datetime.now(timezone.utc)
        if self.repeat_limit is not None:
            if self.repeat_limit == 0:
                raise TaskAlreadyDoneError()
            if self.repeat_limit > 0:
                self.repeat_limit -= 1
        if self.last_completed_at != None:
            match self.repeat_frequency:
                case TaskRepeatFrequency.DAILY:
                    if current_time < self.last_completed_at + timedelta(days=1):
                        raise TaskExecutedTooEarlyError()
                case TaskRepeatFrequency.ONCE_TWO_DAYS:
                    if current_time < self.last_completed_at + timedelta(days=2):
                        raise TaskExecutedTooEarlyError()
                case TaskRepeatFrequency.WEEKLY:
                    if current_time < self.last_completed_at + timedelta(days=7):
                        raise TaskExecutedTooEarlyError()
        self.last_completed_at = current_time

    def calculate_task_rewards(self) -> TaskReward:
        xp = 0
        gold = 0
        if self.type == TaskType.AUTO:
            self._calculate_multipliers()
            xp = self.difficulty_multiplier * 60 + self.priority_multiplier * 40
            gold = self.difficulty_multiplier * 30 + self.priority_multiplier * 20
        elif self.type == TaskType.CUSTOM:
            if self.custom_xp_reward is not None:
                xp = self.custom_xp_reward
            if self.custom_gold_reward is not None:
                gold = self.custom_gold_reward
        return TaskReward(
                xp=xp, 
                gold=gold
            )

    def _calculate_multipliers(self): 
        match self.difficulty:
            case TaskDifficulty.EASY:
                self.difficulty_multiplier = 1
            case TaskDifficulty.MEDIUM:
                self.difficulty_multiplier = 2
            case TaskDifficulty.HARD:
                self.difficulty_multiplier = 3
            case TaskDifficulty.EPIC:
                self.difficulty_multiplier = 4
        match self.priority:
            case TaskPriority.LOW:
                self.priority_multiplier = 1
            case TaskPriority.MEDIUM:
                self.priority_multiplier = 2
            case TaskPriority.HIGH:
                self.priority_multiplier = 3
            case TaskPriority.CRITICAL:
                self.priority_multiplier = 4







# для совместимости


@dataclass
class TaskRewardCalculatorDomain:
    task_type: Optional[TaskType]
    task_difficulty: Optional[TaskDifficulty]
    task_priority: Optional[TaskPriority]
    custom_xp_reward: Optional[int]
    custom_gold_reward: Optional[int]
    difficulty_multiplier: int = field(init=False, default=0)
    priority_multiplier: int = field(init=False, default=0)

    def calculate_task_rewards(self) -> TaskReward:
        xp = 0
        gold = 0
        if self.task_type == TaskType.AUTO:
            self._calculate_multipliers()
            xp = self.difficulty_multiplier * 60 + self.priority_multiplier * 40
            gold = self.difficulty_multiplier * 30 + self.priority_multiplier * 20
        elif self.task_type == TaskType.CUSTOM:
            if self.custom_xp_reward is not None:
                xp = self.custom_xp_reward
            if self.custom_gold_reward is not None:
                gold = self.custom_gold_reward
        return TaskReward(
                xp=xp, 
                gold=gold
            )

    def _calculate_multipliers(self): 
        match self.task_difficulty:
            case TaskDifficulty.EASY:
                self.difficulty_multiplier = 1
            case TaskDifficulty.MEDIUM:
                self.difficulty_multiplier = 2
            case TaskDifficulty.HARD:
                self.difficulty_multiplier = 3
            case TaskDifficulty.EPIC:
                self.difficulty_multiplier = 4
        match self.task_priority:
            case TaskPriority.LOW:
                self.priority_multiplier = 1
            case TaskPriority.MEDIUM:
                self.priority_multiplier = 2
            case TaskPriority.HIGH:
                self.priority_multiplier = 3
            case TaskPriority.CRITICAL:
                self.priority_multiplier = 4

        