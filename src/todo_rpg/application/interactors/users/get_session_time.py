from todo_rpg.application.exceptions import SessionNotFoundError
from todo_rpg.application.interfaces import SessionRepositoryProtocol
from todo_rpg.application.dto.shared import MessageDTO


class GetSessionTimeInteractor:
    def __init__(self, session_repo: SessionRepositoryProtocol) -> None:
        self.session_repo = session_repo

    async def __call__(self, session_token: str | None) -> MessageDTO:
        if session_token is None:
            raise SessionNotFoundError()
        session_time = await self.session_repo.get_session_time(session_token)
        hours = session_time // 3600
        minutes = (session_time % 3600) // 60
        seconds = session_time % 60
        formatted_time = f"hours: {hours}, minutes: {minutes}, seconds: {seconds}"
        return MessageDTO(message=formatted_time)
