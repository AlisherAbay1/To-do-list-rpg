from dotenv import dotenv_values
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import relationship
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


def get_new_session_maker() -> async_sessionmaker[AsyncSession]:
    database_url = f"postgresql+asyncpg://postgres:{dotenv_values(r".env")["DB_PASSWORD"]}@localhost:5432/to-do-list-rpg"
    engine = create_async_engine(database_url)
    
    return async_sessionmaker(bind=engine)

def map_imperativly_models():
    Base.registry.map_imperatively(UserDomain, get_user_table())
    Base.registry.map_imperatively(UserRankDomain, get_rank_table())
    Base.registry.map_imperatively(SkillDomain, get_skill_table())
    Base.registry.map_imperatively(ItemDomain, get_item_table(), 
                                   properties={
                                       "skills": relationship(SkillDomain, secondary="items_to_skills", lazy="noload")
                                   })
    Base.registry.map_imperatively(TaskDomain, get_task_table(),
                                   properties={
                                            "user": relationship(UserDomain, passive_deletes=True, lazy="noload"),
                                            "skills": relationship(SkillDomain, secondary="tasks_to_skills", lazy="noload"),
                                            "items": relationship(ItemDomain, secondary="tasks_to_items", lazy="noload")
                                            })
    Base.registry.map_imperatively(TaskCategoryDomain, get_task_category_table())
    Base.registry.map_imperatively(TaskHistoryDomain, get_task_history_table(),
                                   properties={
                                       "skills": relationship(SkillDomain, secondary="tasks_history_to_skills", lazy="noload"),
                                       "items": relationship(ItemDomain, secondary="tasks_history_to_items", lazy="noload")
                                   })
    Base.registry.map_imperatively(ItemHistoryDomain, get_item_usage_history_table())
    Base.registry.map_imperatively(ShopDomain, get_shop_table())
    Base.registry.map_imperatively(InventoryDomain, get_inventory_table())