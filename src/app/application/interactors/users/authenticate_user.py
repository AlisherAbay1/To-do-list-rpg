from src.app.application.interfaces.repositories_interfaces import UserRepositoryProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.dto.users import LoginIdentifierDTO, CreateUserResultDTO
from src.app.core.security import password_verify
from src.app.application.exceptions import UserNotFoundError, IncorrectPasswordError

class AuthenticateUserInteractor:
    def __init__(self, repo: UserRepositoryProtocol, cash_repo: RedisRepositoryProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, dto: LoginIdentifierDTO):
        if "@" in dto.username_or_email:
            user = await self.repo.get_user_by_email(dto.username_or_email)
        else:
            user = await self.repo.get_user_by_username(dto.username_or_email)
        if user is None:
            raise UserNotFoundError()
        if not password_verify(dto.password, user.password):
            raise IncorrectPasswordError()
        session_token = await self.cash_repo.create_session(str(user.id))
        return CreateUserResultDTO(
            username=user.username, 
            email=user.email, 
            session_token=session_token
        )