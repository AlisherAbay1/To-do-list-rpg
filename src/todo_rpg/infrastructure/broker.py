from taskiq_redis import RedisStreamBroker
from taskiq.middlewares import SmartRetryMiddleware
from todo_rpg.infrastructure.config import config
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from dishka.integrations.taskiq import setup_dishka
from todo_rpg.infrastructure.di import get_dishka_container

broker = RedisStreamBroker(
    url=f"redis://{config.redis.host}:{config.redis.port}"
).with_middlewares(SmartRetryMiddleware())

schedule = TaskiqScheduler(broker=broker, sources=[LabelScheduleSource(broker)])

container = get_dishka_container()

setup_dishka(broker=broker, container=container)
