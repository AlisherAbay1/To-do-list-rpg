from todo_rpg.application.interfaces import SessionRepositoryProtocol


class DeleteSessionInteractor:
    def __init__(self, session_repo: SessionRepositoryProtocol) -> None:
        self.session_repo = session_repo

    async def __call__(self, session_token: str) -> None:
        await self.session_repo.delete_session(session_token)
