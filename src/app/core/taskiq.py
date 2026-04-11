from taskiq import TaskiqScheduler
from taskiq_redis import RedisStreamBroker
from taskiq.middlewares import SmartRetryMiddleware
from taskiq.schedule_sources import LabelScheduleSource

broker = RedisStreamBroker(url="redis://localhost:6379").with_middlewares(SmartRetryMiddleware())

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)]
)