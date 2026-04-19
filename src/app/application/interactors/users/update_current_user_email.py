from src.app.application.interfaces.repositories_interfaces import UserRepositoryProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.dto.users import UserEmailDTO
from src.app.application.exceptions import SessionNotFoundError, UserNotFoundError, IncorrectPasswordError, EmailAlreadyTakenError
from src.app.core.security import password_verify
from uuid import UUID


class UpdateCurrentUserEmailInteractor:
    def __init__(self, repo: UserRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, dto: UserEmailDTO, session_token: str):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.repo.get_user(UUID(user_id))
        if not user:
            raise UserNotFoundError()
        if not password_verify(dto.password, user.password):
            raise IncorrectPasswordError()
        if await self.repo.get_user_by_email(dto.new_email):
            raise EmailAlreadyTakenError()
        user.email = dto.new_email
        await self.repo.update(user)
        await self.transaction.commit()
        return dto.new_email