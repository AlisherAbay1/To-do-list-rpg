from fastapi import FastAPI
from .users import router as users_router
from .tasks import router as tasks_router
from .skills import router as skills_router
from .items import router as items_router
from .auth import router as auth_router

app = FastAPI()
app.include_router(router=users_router, tags=["users"])
app.include_router(router=tasks_router, tags=["tasks"])
app.include_router(router=skills_router, tags=["skills"])
app.include_router(router=items_router, tags=["items"])
app.include_router(router=auth_router, tags=["auth"])

