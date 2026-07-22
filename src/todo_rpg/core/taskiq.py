from taskiq import TaskiqScheduler
from taskiq_redis import RedisStreamBroker
from taskiq.middlewares import SmartRetryMiddleware
from taskiq.schedule_sources import LabelScheduleSource
from todo_rpg.infrastructure.config import config

broker = RedisStreamBroker(
    url=f"redis://{config.redis.host}:{config.redis.port}"
).with_middlewares(SmartRetryMiddleware())

scheduler = TaskiqScheduler(broker=broker, sources=[LabelScheduleSource(broker)])
