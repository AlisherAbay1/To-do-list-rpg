from src.app.domain.enums import TaskType, TaskDifficulty, TaskPriority
from src.app.application.dto.tasks import TaskReward
from typing import Optional

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

        