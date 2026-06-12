from todo_rpg.core.taskiq import broker
from todo_rpg.application.interactors import (
    ClearExpiredSkillsInteractor,
    ClearExpiredTasksInteractor,
)
from dishka.integrations.taskiq import FromDishka


@broker.task(schedule=[{"cron": "0 3 * * *"}])
async def cleanup_expired_skills_task(
    interactor: FromDishka[ClearExpiredSkillsInteractor],
):
    await interactor()


@broker.task(schedule=[{"cron": "0 3 * * *"}])
async def cleanup_expired_tasks_task(
    interactor: FromDishka[ClearExpiredTasksInteractor],
):
    await interactor()
