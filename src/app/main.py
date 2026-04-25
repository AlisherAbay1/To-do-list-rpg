from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from src.app.presentation.api.routers.users import router as users_router
from src.app.presentation.api.routers.tasks import router as tasks_router
from src.app.presentation.api.routers.skills import router as skills_router
from src.app.presentation.api.routers.items import router as items_router
from src.app.presentation.api.routers.inventory import router as inventory_router
from src.app.presentation.api.routers.shop import router as shop_router
from src.app.presentation.exception_handlers import register_exeptions
from src.app.core.taskiq import broker
from sqlalchemy.orm import relationship
from contextlib import asynccontextmanager
from src.app.infrastructure.di_providers import AppProvider, UserProvider, TaskProvider, SkillProvider, ItemProvider
from src.app.infrastructure.database.models import (
    get_user_table, get_rank_table, get_task_table,
    get_task_history_table, get_task_category_table, get_skill_table,
    get_shop_table, get_item_table, get_item_usage_history_table,
    get_inventory_table, Base
)
from src.app.domain import (
    UserDomain, TaskDomain, TaskCategoryDomain,
    TaskHistoryDomain, SkillDomain, UserRankDomain,
    ItemDomain, ItemHistoryDomain, ShopDomain,
    InventoryDomain
)

def map_imperativly_models():
    Base.registry.map_imperatively(UserDomain, get_user_table())
    Base.registry.map_imperatively(UserRankDomain, get_rank_table())
    Base.registry.map_imperatively(TaskDomain, get_task_table(),
                                   properties={
                                            "user": relationship(UserDomain, passive_deletes=True, lazy="noload"),
                                            "skills": relationship(SkillDomain, secondary="tasks_to_skills", lazy="noload"),
                                            "items": relationship(ItemDomain, secondary="tasks_to_items", lazy="noload"),
                                            })
    Base.registry.map_imperatively(TaskCategoryDomain, get_task_category_table())
    Base.registry.map_imperatively(TaskHistoryDomain, get_task_history_table(),
                                   properties={
                                       relationship(secondary="tasks_history_to_skills", lazy="noload")
                                   })
    Base.registry.map_imperatively(SkillDomain, get_skill_table())
    Base.registry.map_imperatively(ItemDomain, get_item_table())
    Base.registry.map_imperatively(ItemHistoryDomain, get_item_usage_history_table())
    Base.registry.map_imperatively(ShopDomain, get_shop_table())
    Base.registry.map_imperatively(InventoryDomain, get_inventory_table())

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