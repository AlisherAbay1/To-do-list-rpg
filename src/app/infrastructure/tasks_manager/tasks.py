from src.app.core.taskiq import broker
from src.app.application.interactors.skills import ClearExpiredSkillsInteractor
from dishka.integrations.taskiq import FromDishka

@broker.task(schedule=[{"cron": "0 3 * * *"}])
async def cleanup_expired_skills_task(
    interactor: FromDishka[ClearExpiredSkillsInteractor]):
    await interactor()