from src.app.domain.enums import TaskType, TaskDifficulty, TaskPriority
from src.app.application.dto.tasks import TaskReward
from src.app.domain.enums import TaskRepeatFrequency
from src.app.application.exceptions import TaskAlreadyDoneError, TaskExecutedTooEarlyError
from uuid import UUID
from datetime import datetime, timezone, timedelta
from typing import Optional

class TaskDomain:
    def __init__(
            self, 
            id: UUID,
            user_id: UUID,
            title: str,
            description: Optional[str],
            category_id: Optional[UUID],
            repeat_limit: Optional[int],
            repeat_frequency: Optional[TaskRepeatFrequency],
            deadline: Optional[datetime],
            last_completed_at: Optional[datetime],
            created_at: datetime,
            type: Optional[TaskType],
            difficulty: Optional[TaskDifficulty],
            priority: Optional[TaskPriority],
            custom_xp_reward: Optional[int],
            custom_gold_reward: Optional[int]
            ) -> None:
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.category_id = category_id
        self.repeat_limit = repeat_limit
        self.repeat_frequency = repeat_frequency
        self.deadline = deadline
        self.last_completed_at = last_completed_at
        self.created_at = created_at
        self.type = type
        self.difficulty = difficulty
        self.priority = priority
        self.custom_xp_reward = custom_xp_reward
        self.custom_gold_reward = custom_gold_reward

        self.difficulty_multiplier = 0
        self.priority_multiplier = 0

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










class TaskRewardCalculatorDomain:
    def __init__(
            self, 
            task_type: Optional[TaskType], 
            task_difficulty: Optional[TaskDifficulty], 
            task_priority: Optional[TaskPriority], 
            custom_xp_reward: Optional[int], 
            custom_gold_reward: Optional[int]
            ) -> None:
        self.task_type = task_type
        self.task_difficulty = task_difficulty
        self.task_priority = task_priority
        self.custom_xp_reward = custom_xp_reward
        self.custom_gold_reward = custom_gold_reward
        self.difficulty_multiplier = 0
        self.priority_multiplier = 0

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

        