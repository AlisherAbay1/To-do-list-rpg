from taskiq_redis import RedisStreamBroker
from taskiq.middlewares import SmartRetryMiddleware
from todo_rpg.infrastructure.config import config
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource


broker = RedisStreamBroker(
    url=f"redis://{config.redis.host}:{config.redis.port}"
).with_middlewares(SmartRetryMiddleware())

schedule = TaskiqScheduler(broker=broker, sources=[LabelScheduleSource(broker)])
