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
from todo_rpg.presentation.api.routers.user_ranks import router as user_ranks_router
from todo_rpg.presentation.api.routers.shop_transaction import (
    router as shop_transactions_router,
)
from todo_rpg.presentation.exception_handlers import register_exeptions
from todo_rpg.core.taskiq import broker
from contextlib import asynccontextmanager
import asyncio
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
    UserRankProvider,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not broker.is_worker_process:
        await broker.startup()
    yield
    await app.state.dishka_container.close()
    if not broker.is_worker_process:
        await broker.shutdown()


async def set_up_fastapi_routers(app: FastAPI):
    app.include_router(router=users_router, tags=["users"])
    app.include_router(router=tasks_router, tags=["tasks"])
    app.include_router(router=skills_router, tags=["skills"])
    app.include_router(router=items_router, tags=["items"])
    app.include_router(router=inventory_router, tags=["inventory"])
    app.include_router(router=shop_router, tags=["shop"])
    app.include_router(router=task_categories_router, tags=["task_categories"])
    app.include_router(router=stats_router, tags=["stats"])
    app.include_router(router=user_ranks_router, tags=["user_ranks"])
    app.include_router(router=shop_transactions_router, tags=["shop_transactions"])


async def get_dishka_container():
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
        UserRankProvider(),
    )
    return container


async def main():
    app = FastAPI(lifespan=lifespan)
    set_up_fastapi_routers(app)
    register_exeptions(app)
    container = get_dishka_container()
    setup_dishka(container, app)


if __name__ == "__main__":
    asyncio.run(main())
