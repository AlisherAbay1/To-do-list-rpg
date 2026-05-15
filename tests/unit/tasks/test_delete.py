import pytest_check
from tests.fabrics import make_task


def test_task_delete():
    task = make_task()
    task.delete()
    pytest_check.equal(task.deleted, True)
    pytest_check.not_equal(task.deleted_at, None)
