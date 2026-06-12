import pytest
from tests.fabrics import make_task
from todo_rpg.application.exceptions import (
    TaskAlreadyDoneError,
    TaskExecutedTooEarlyError,
)
from datetime import datetime, timezone
from todo_rpg.domain.enums import TaskRepeatFrequency


def test_repeat_limit():
    task = make_task(repeat_limit=7)
    task.complete()
    assert task.repeat_limit == 6


def test_task_already_done_error():
    task = make_task(repeat_limit=0)
    with pytest.raises(TaskAlreadyDoneError):
        task.complete()


@pytest.mark.parametrize(
    "repeat_frequency",
    [
        TaskRepeatFrequency.DAILY,
        TaskRepeatFrequency.ONCE_TWO_DAYS,
        TaskRepeatFrequency.WEEKLY,
    ],
)
def test_task_executed_too_early_error(repeat_frequency: TaskRepeatFrequency):
    task = make_task(
        last_completed_at=datetime.now(tz=timezone.utc),
        repeat_frequency=repeat_frequency,
    )
    with pytest.raises(TaskExecutedTooEarlyError):
        task.complete()


def test_if_time_updated():
    task = make_task()
    previus_time = task.last_completed_at
    task.complete()
    assert previus_time != task.last_completed_at
