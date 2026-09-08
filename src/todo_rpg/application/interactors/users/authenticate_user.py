from todo_rpg.application.dto.common.users import UserAuthDTO, SignInDTO
from todo_rpg.application.exceptions import UserNotFoundError
from todo_rpg.domain.exceptions import IncorrectPasswordError
from todo_rpg.application.interfaces import (
    UserRepositoryProtocol,
    RedisRepositoryProtocol,
    PasswordManagerProtocol,
)
from todo_rpg.application.mappers.common import UserMapper


class AuthenticateUserInteractor:
    def __init__(
        self,
        repo: UserRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        password_manager: PasswordManagerProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.password_manager = password_manager

    async def __call__(self, dto: SignInDTO) -> UserAuthDTO:
        if "@" in dto.username_or_email:
            user = await self.repo.get_user_by_email(dto.username_or_email)
        else:
            user = await self.repo.get_user_by_username(dto.username_or_email)
        if user is None:
            raise UserNotFoundError()
        if not self.password_manager.password_verify(dto.password, user.password):
            raise IncorrectPasswordError()
        session_token = await self.cash_repo.create_session(str(user.id))
        return UserMapper.to_auth_dto(domain=user, session_token=session_token)
