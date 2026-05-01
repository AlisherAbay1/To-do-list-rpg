from uuid6 import uuid7

from src.app.application.dto.common.users import CreateUserDTO, UserAuthDTO
from src.app.application.exceptions import (EmailAlreadyTakenError,
                                            UsernameAlreadyTakenError)
from src.app.application.interfaces.cash_interfaces import \
    RedisRepositoryProtocol
from src.app.application.interfaces.repositories_interfaces import \
    UserRepositoryProtocol
from src.app.application.interfaces.transaction_interfaces import \
    TransactionProtocol
from src.app.core.security import hash_password
from src.app.domain import User
from src.app.application.mappers.common import UserMapper

class CreateUserInteractor:
    def __init__(self, repo: UserRepositoryProtocol, cash_repo: RedisRepositoryProtocol, transaction: TransactionProtocol) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, dto: CreateUserDTO) -> UserAuthDTO:
        if await self.repo.does_username_exists(dto.username):
            raise UsernameAlreadyTakenError()
        if await self.repo.does_email_exists(dto.email):
            raise EmailAlreadyTakenError()
        hashed_password = hash_password(dto.password)
        user = User(
            username=dto.username, 
            email=dto.email,
            password=hashed_password, 
        )
        self.repo.save(user)
        
        session_token = await self.cash_repo.create_session(str(user.id))
        user_result = UserMapper.to_auth_dto(
            domain=user, 
            session_token=session_token
        )

        await self.transaction.commit()
        return user_result