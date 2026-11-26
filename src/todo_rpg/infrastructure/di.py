from dishka import AsyncContainer, make_async_container
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


def get_dishka_container() -> AsyncContainer:
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
