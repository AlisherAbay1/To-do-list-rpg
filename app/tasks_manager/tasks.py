from app.core.taskiq import broker
from app.services.interactors.skills import ClearExpiredSkillsInteractor
from app.repositories import SkillRepository, TransactionAlchemyManager
from app.core.database import get_local_session
from taskiq import TaskiqDepends
from sqlalchemy.ext.asyncio import AsyncSession

@broker.task(schedule=[{"cron": "0 3 * * *"}])
async def cleanup_expired_skills_task(
    session: AsyncSession = TaskiqDepends(get_local_session)):
    interactor = ClearExpiredSkillsInteractor(SkillRepository(session), TransactionAlchemyManager(session))
    await interactor()