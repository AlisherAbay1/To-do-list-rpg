from .users import router as users_router
from .tasks import router as tasks_router
from .skills import router as skills_router
from .items import router as items_router
from .inventory import router as inventory_router
from .shop import router as shop_router
from .task_categories import router as task_categories_router
from .stats import router as stats_router
from .user_ranks import router as user_ranks_router
from .shop_transaction import router as shop_transactions_router

__all__ = (
    "users_router",
    "tasks_router",
    "skills_router",
    "items_router",
    "inventory_router",
    "shop_router",
    "task_categories_router",
    "stats_router",
    "user_ranks_router",
    "shop_transactions_router",
)
