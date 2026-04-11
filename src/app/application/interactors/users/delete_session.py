from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol

class DeleteSessionInteractor:
    def __init__(self, cash_repo: RedisRepositoryProtocol) -> None:
        self.cash_repo = cash_repo

    async def __call__(self, session_token: str) -> None:
        await self.cash_repo.delete_session(session_token)