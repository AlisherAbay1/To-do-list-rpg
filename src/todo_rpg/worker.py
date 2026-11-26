from dishka.integrations.taskiq import setup_dishka
from todo_rpg.infrastructure.di import get_dishka_container
from todo_rpg.infrastructure.broker import broker
from taskiq import TaskiqEvents
import todo_rpg.infrastructure.broker_tasks  # noqa: F401

container = get_dishka_container()

setup_dishka(broker=broker, container=container)


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def startup():
    await container.close()
