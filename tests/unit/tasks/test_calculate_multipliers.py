from todo_rpg.domain.enums import TaskDifficulty, TaskPriority
from tests.fabrics import make_task
import pytest
import pytest_check


@pytest.mark.parametrize(
    (
        "difficulty",
        "priority",
        "expected_difficulty_multiplier",
        "expected_priority_multiplier",
    ),
    (
        (TaskDifficulty.EASY, TaskPriority.LOW, 1, 1),
        (TaskDifficulty.MEDIUM, TaskPriority.LOW, 2, 1),
        (TaskDifficulty.EASY, TaskPriority.HIGH, 1, 3),
        (TaskDifficulty.MEDIUM, TaskPriority.HIGH, 2, 3),
        (TaskDifficulty.EPIC, TaskPriority.CRITICAL, 4, 4),
        (None, None, 0, 0),
    ),
)
def test_calculate_multipliers(
    difficulty: TaskDifficulty,
    priority: TaskPriority,
    expected_difficulty_multiplier: int,
    expected_priority_multiplier: int,
):
    task = make_task(difficulty=difficulty, priority=priority)
    calculations = task._calculate_multipliers()
    pytest_check.equal(calculations[0], expected_difficulty_multiplier)
    pytest_check.equal(calculations[1], expected_priority_multiplier)
