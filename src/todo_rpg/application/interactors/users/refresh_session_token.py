from todo_rpg.application.exceptions import SessionNotFoundError
from todo_rpg.application.interfaces import SessionRepositoryProtocol
from todo_rpg.application.dto.shared import MessageDTO


class RefreshSessionTokenInteractor:
    def __init__(self, session_repo: SessionRepositoryProtocol) -> None:
        self.session_repo = session_repo

    async def __call__(self, session_token: str | None) -> MessageDTO:
        if session_token is None:
            raise SessionNotFoundError()
        await self.session_repo.extend_token_time(session_token)
        return MessageDTO(message="time extended")
