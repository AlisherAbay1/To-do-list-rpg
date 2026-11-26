from todo_rpg.application.interactors import (
    ClearExpiredSkillsInteractor,
    ClearExpiredTasksInteractor,
)
from todo_rpg.infrastructure.broker import broker
from dishka.integrations.taskiq import FromDishka, inject


@inject(patch_module=True)
@broker.task(schedule=[{"cron": "0 3 * * *"}])
async def cleanup_expired_skills_task(
    interactor: FromDishka[ClearExpiredSkillsInteractor],
):
    await interactor()


@inject(patch_module=True)
@broker.task(schedule=[{"cron": "0 3 * * *"}])
async def cleanup_expired_tasks_task(
    interactor: FromDishka[ClearExpiredTasksInteractor],
):
    await interactor()
