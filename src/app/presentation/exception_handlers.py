from src.app.application.exceptions import UserNotFoundError, EmailAlreadyTakenError, IncorrectPasswordError, \
                            TaskNotFoundError, TaskAlreadyDoneError, SkillNotFoundError, \
                            ItemNotFoundError, UsernameAlreadyTakenError, SessionNotFoundError, \
                            TaskAccessDeniedError, TaskExecutedTooEarlyError, TaskNotFoundInHistoryError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

def register_exeptions(app: FastAPI):
    @app.exception_handler(UserNotFoundError)
    async def user_not_found(request: Request, exc: UserNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "User not found"})

    @app.exception_handler(EmailAlreadyTakenError)
    async def email_already_taken(request: Request, exc: EmailAlreadyTakenError):
        return JSONResponse(status_code=409, content={"detail": "Email already taken"})

    @app.exception_handler(IncorrectPasswordError)
    async def incorrect_password(request: Request, exc: IncorrectPasswordError):
        return JSONResponse(status_code=401, content={"detail": "Incorrect password"})

    @app.exception_handler(TaskNotFoundError)
    async def task_not_found(request: Request, exc: TaskNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Task not found"})

    @app.exception_handler(TaskExecutedTooEarlyError)
    async def task_executed_too_early(request: Request, exc: TaskNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Task executed too early"})

    @app.exception_handler(TaskAlreadyDoneError)
    async def task_already_done(request: Request, exc: TaskAlreadyDoneError):
        return JSONResponse(status_code=409, content={"detail": "Task repeat limit is 0"})

    @app.exception_handler(SkillNotFoundError)
    async def skill_not_found(request: Request, exc: SkillNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Skill not found"})

    @app.exception_handler(TaskNotFoundInHistoryError)
    async def task_not_found_in_history(request: Request, exc: SkillNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Task not found in task history"})

    @app.exception_handler(ItemNotFoundError)
    async def item_not_found(request: Request, exc: ItemNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Item not found"})

    @app.exception_handler(UsernameAlreadyTakenError)
    async def username_already_exists(request: Request, exc: UsernameAlreadyTakenError):
        return JSONResponse(status_code=409, content={"detail": "Username already taken"})

    @app.exception_handler(SessionNotFoundError)
    async def session_not_found(request: Request, exc: SessionNotFoundError):
        return JSONResponse(status_code=401, content={"detail": "Session not found"})

    @app.exception_handler(TaskAccessDeniedError)
    async def task_access_denied(request: Request, exc: TaskAccessDeniedError):
        return JSONResponse(status_code=403, content={"detail": "Task access denied"})