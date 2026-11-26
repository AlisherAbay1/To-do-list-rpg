from todo_rpg.application.exceptions import UserNotFoundError
from todo_rpg.application.interfaces import (
    UserRepositoryProtocol,
    UoWProtocol,
    SessionRepositoryProtocol,
)


class DeleteCurrentUserInteractor:
    def __init__(
        self,
        repo: UserRepositoryProtocol,
        session_repo: SessionRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.session_repo = session_repo
        self.uow = uow

    async def __call__(self, session_token) -> None:
        user_id = await self.session_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise UserNotFoundError()
        await self.repo.delete(user_id)
        await self.uow.commit()
