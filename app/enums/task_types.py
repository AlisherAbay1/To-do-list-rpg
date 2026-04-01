from enum import Enum

class TaskRepeatFrequency(Enum):
    DAILY = "DAILY"
    ONCE_TWO_DAYS = "ONCE-TWO-DAYS"
    WEEKLY = "WEEKLY"

class TaskType(Enum):
    CUSTOM = "CUSTOM"
    AUTO = "AUTO"

class TaskDifficulty(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    EPIC = "EPIC"

class TaskPriority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"