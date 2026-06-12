from todo_rpg.domain.enums import TaskDifficulty, TaskPriority, TaskType
from tests.fabrics import make_task
import pytest
import pytest_check
from typing import Optional


@pytest.mark.parametrize(
    ("difficulty", "priority", "xp", "gold"),
    (
        (TaskDifficulty.EASY, TaskPriority.LOW, 100, 50),
        (TaskDifficulty.EPIC, TaskPriority.CRITICAL, 400, 200),
        (TaskDifficulty.HARD, TaskPriority.MEDIUM, 260, 130),
        (TaskDifficulty.EPIC, TaskPriority.LOW, 280, 140),
        (None, None, 0, 0),
    ),
)
def test_task_auto_calcuation(
    difficulty: TaskDifficulty, priority: TaskPriority, xp: int, gold: int
):
    task = make_task(type=TaskType.AUTO, difficulty=difficulty, priority=priority)
    reward = task.calculate_task_rewards()
    pytest_check.equal(reward.xp, xp)
    pytest_check.equal(reward.gold, gold)


def test_task_default_auto_calculation():
    task = make_task(difficulty=TaskDifficulty.MEDIUM, priority=TaskPriority.MEDIUM)
    reward = task.calculate_task_rewards()
    pytest_check.equal(reward.xp, 200)
    pytest_check.equal(reward.gold, 100)


def test_task_custom_calculation():
    task = make_task(type=TaskType.CUSTOM, custom_xp_reward=77, custom_gold_reward=77)
    reward = task.calculate_task_rewards()
    pytest_check.equal(reward.xp, 77)
    pytest_check.equal(reward.gold, 77)


@pytest.mark.parametrize(
    ("xp", "gold", "expected_xp", "expected_gold"),
    ((None, 10, 0, 10), (10, None, 10, 0), (None, None, 0, 0), (10, 10, 10, 10)),
)
def test_task_custom_none_calculation(
    xp: Optional[int], gold: Optional[int], expected_xp: int, expected_gold: int
):
    task = make_task(type=TaskType.CUSTOM, custom_xp_reward=xp, custom_gold_reward=gold)
    reward = task.calculate_task_rewards()
    pytest_check.equal(reward.xp, expected_xp)
    pytest_check.equal(reward.gold, expected_gold)
