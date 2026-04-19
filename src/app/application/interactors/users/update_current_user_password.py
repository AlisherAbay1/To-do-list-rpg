from src.app.application.interfaces.repositories_interfaces import UserRepositoryProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.dto.users import UserPasswordDTO
from src.app.core.security import password_verify, hash_password
from src.app.application.exceptions import SessionNotFoundError, UserNotFoundError, IncorrectPasswordError
from uuid import UUID

class UpdateCurrentUserPasswordInteractor:
    def __init__(self, repo: UserRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, dto: UserPasswordDTO, session_token: str):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.repo.get_user(UUID(user_id))
        if not user:
            raise UserNotFoundError()
        if not password_verify(dto.old_password, user.password): 
            raise IncorrectPasswordError()
        user.password = hash_password(dto.new_password)
        await self.repo.update(user)
        await self.transaction.commit()