from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from todo_rpg.presentation.api.routers.users import router as users_router
from todo_rpg.presentation.api.routers.tasks import router as tasks_router
from todo_rpg.presentation.api.routers.skills import router as skills_router
from todo_rpg.presentation.api.routers.items import router as items_router
from todo_rpg.presentation.api.routers.inventory import router as inventory_router
from todo_rpg.presentation.api.routers.shop import router as shop_router
from todo_rpg.presentation.api.routers.task_categories import (
    router as task_categories_router,
)
from todo_rpg.presentation.api.routers.stats import router as stats_router
from todo_rpg.presentation.exception_handlers import register_exeptions
from todo_rpg.core.taskiq import broker
from contextlib import asynccontextmanager
from todo_rpg.infrastructure.di_providers import (
    AppProvider,
    UserProvider,
    TaskProvider,
    SkillProvider,
    ItemProvider,
    TaskCategoriesProvider,
    StatsProvider,
    ShopProvider,
    InventoryProvider,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not broker.is_worker_process:
        await broker.startup()
    yield
    await app.state.dishka_container.close()
    if not broker.is_worker_process:
        await broker.shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(router=users_router, tags=["users"])
app.include_router(router=tasks_router, tags=["tasks"])
app.include_router(router=skills_router, tags=["skills"])
app.include_router(router=items_router, tags=["items"])
app.include_router(router=inventory_router, tags=["inventory"])
app.include_router(router=shop_router, tags=["shop"])
app.include_router(router=task_categories_router, tags=["task_categories"])
app.include_router(router=stats_router, tags=["stats"])

register_exeptions(app)

container = make_async_container(
    AppProvider(),
    UserProvider(),
    TaskProvider(),
    SkillProvider(),
    ItemProvider(),
    TaskCategoriesProvider(),
    StatsProvider(),
    ShopProvider(),
    InventoryProvider(),
)
setup_dishka(container, app)
