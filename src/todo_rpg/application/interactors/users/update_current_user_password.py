from todo_rpg.application.dto.common.users import UserPasswordDTO
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    UserNotFoundError,
)
from todo_rpg.domain.exceptions import IncorrectPasswordError
from todo_rpg.application.interfaces import (
    UserRepositoryProtocol,
    SessionRepositoryProtocol,
    PasswordManagerProtocol,
    UoWProtocol,
)


class UpdateCurrentUserPasswordInteractor:
    def __init__(
        self,
        repo: UserRepositoryProtocol,
        session_repo: SessionRepositoryProtocol,
        password_manager: PasswordManagerProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.session_repo = session_repo
        self.password_manager = password_manager
        self.uow = uow

    async def __call__(self, dto: UserPasswordDTO, session_token: str) -> None:
        user_id = await self.session_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.repo.get_user(user_id)
        if not user:
            raise UserNotFoundError()
        if not self.password_manager.password_verify(dto.old_password, user.password):
            raise IncorrectPasswordError()
        user.password = self.password_manager.hash_password(dto.new_password)
        await self.uow.commit()
