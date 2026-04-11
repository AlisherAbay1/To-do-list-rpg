from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.exceptions import SessionNotFoundError

class RefreshSessionTokenInteractor:
    def __init__(self, cash_repo: RedisRepositoryProtocol) -> None:
        self.cash_repo = cash_repo

    async def __call__(self, session_token: str | None):
        if session_token is None:
            raise SessionNotFoundError()
        await self.cash_repo.extend_token_time(session_token)
        return {"message": "time extended"}