from uuid import UUID

from todo_rpg.application.interfaces import (
    ItemRepositoryProtocol,
    UserRepositoryProtocol,
    SessionRepositoryProtocol,
    UoWProtocol,
)

from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    UserNotFoundError,
    AccessDeniedError,
)


class DeleteItemInteractor:
    def __init__(
        self,
        repo: ItemRepositoryProtocol,
        user_repo: UserRepositoryProtocol,
        session_repo: SessionRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.user_repo = user_repo
        self.session_repo = session_repo
        self.uow = uow

    async def __call__(self, item_id: UUID, session_token: str) -> None:
        user_id = await self.session_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.user_repo.get_user(user_id)
        if user is None:
            raise UserNotFoundError()
        if not user.is_admin:
            raise AccessDeniedError()

        await self.repo.delete(item_id)
        await self.uow.commit()
