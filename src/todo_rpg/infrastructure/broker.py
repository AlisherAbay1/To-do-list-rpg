from taskiq.abc.broker import AsyncBroker
from taskiq_redis import RedisStreamBroker
from taskiq.middlewares import SmartRetryMiddleware
from todo_rpg.infrastructure.config import config
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource


async def _get_redis_broker():
    broker = RedisStreamBroker(
        url=f"redis://{config.redis.host}:{config.redis.port}"
    ).with_middlewares(SmartRetryMiddleware())
    return broker


async def _get_scheduler(broker: AsyncBroker):
    scheduler = TaskiqScheduler(broker=broker, sources=[LabelScheduleSource(broker)])
    return scheduler


broker = _get_redis_broker()
schedule = _get_scheduler(broker)
