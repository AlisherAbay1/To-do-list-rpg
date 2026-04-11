from src.app.application.interfaces.repositories_interfaces import UserRepositoryProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.dto.users import CreateUserDTO, CreateUserResultDTO
from src.app.core.security import hash_password
from src.app.application.exceptions import UsernameAlreadyTakenError, EmailAlreadyTakenError
from src.app.infrastructure.database.models import User
from uuid_utils import uuid7

class CreateUserInteractor:
    def __init__(self, repo: UserRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, dto: CreateUserDTO) -> CreateUserResultDTO:
        if await self.repo.does_username_exists(dto.username):
            raise UsernameAlreadyTakenError()
        if await self.repo.does_email_exists(dto.email):
            raise EmailAlreadyTakenError()
        hashed_password = hash_password(dto.password)
        user = User(
            id=uuid7(),
            username=dto.username, 
            email=dto.email,
            password=hashed_password, 
        )
        self.repo.save(user)
        
        session_token = await self.cash_repo.create_session(str(user.id))
        user_result = CreateUserResultDTO(
            username=user.username, 
            email=user.email, 
            session_token=session_token
        )

        await self.transaction.commit()
        return user_result