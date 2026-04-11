from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.exceptions import SessionNotFoundError

class GetSessionTimeInteractor:
    def __init__(self, cash_repo: RedisRepositoryProtocol) -> None:
        self.cash_repo = cash_repo

    async def __call__(self, session_token: str | None):
        if session_token is None:
            raise SessionNotFoundError()
        session_time = await self.cash_repo.get_session_time(session_token)
        hours = session_time // 3600
        minutes = (session_time % 3600) // 60
        seconds = session_time % 60
        formated_time = f"hours: {hours}, minutes: {minutes}, seconds: {seconds}"
        return {"message": formated_time}