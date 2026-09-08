from todo_rpg.application.dto.common.users import UserEmailDTO
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    UserNotFoundError,
)
from todo_rpg.domain.exceptions import (
    EmailAlreadyTakenError,
    IncorrectPasswordError,
)
from todo_rpg.application.interfaces import (
    UserRepositoryProtocol,
    RedisRepositoryProtocol,
    UoWProtocol,
    PasswordManagerProtocol,
)


class UpdateCurrentUserEmailInteractor:
    def __init__(
        self,
        repo: UserRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
        password_manager: PasswordManagerProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.uow = uow
        self.password_manager = password_manager

    async def __call__(self, dto: UserEmailDTO, session_token: str) -> str:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.repo.get_user(user_id)
        if not user:
            raise UserNotFoundError()
        if not self.password_manager.password_verify(dto.password, user.password):
            raise IncorrectPasswordError()
        if await self.repo.get_user_by_email(dto.new_email):
            raise EmailAlreadyTakenError()
        user.email = dto.new_email
        await self.uow.commit()
        return dto.new_email
