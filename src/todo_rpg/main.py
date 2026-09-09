from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from todo_rpg.presentation.api.routers import (
    users_router,
    shop_router,
    items_router,
    stats_router,
    tasks_router,
    skills_router,
    inventory_router,
    user_ranks_router,
    task_categories_router,
    shop_transactions_router,
)
from todo_rpg.presentation.exception_handlers import register_exeptions
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
    yield
    await app.state.dishka_container.close()


async def setup_fastapi_routers(app: FastAPI):
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
    setup_fastapi_routers(app)
    register_exeptions(app)
    container = get_dishka_container()
    setup_dishka(container, app)


if __name__ == "__main__":
    asyncio.run(main())
