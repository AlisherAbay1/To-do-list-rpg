from dataclasses import dataclass


@dataclass(slots=True)
class TaskReward:
    xp: int
    gold: int
