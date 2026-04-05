from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from app.api.routers.users import router as users_router
from app.api.routers.tasks import router as tasks_router
from app.api.routers.skills import router as skills_router
from app.api.routers.items import router as items_router
from app.api.routers.inventory import router as inventory_router
from app.api.routers.shop import router as shop_router
from app.api.exception_handlers import register_exeptions
from app.core.taskiq import broker
from contextlib import asynccontextmanager
from app.ioc import AppProvider, UserProvider, TaskProvider, SkillProvider, ItemProvider




@asynccontextmanager
async def lifespan(app: FastAPI):
    if not broker.is_worker_process:
        await broker.startup()
    yield
    if not broker.is_worker_process:
        await broker.shutdown()

app = FastAPI(lifespan=lifespan)

app.include_router(router=users_router, tags=["users"])
app.include_router(router=tasks_router, tags=["tasks"])
app.include_router(router=skills_router, tags=["skills"])
app.include_router(router=items_router, tags=["items"])
app.include_router(router=inventory_router, tags=["inventory"])
app.include_router(router=shop_router, tags=["shop"])

register_exeptions(app)

container = make_async_container(AppProvider(), UserProvider(), TaskProvider(), SkillProvider(), ItemProvider())
setup_dishka(container, app)