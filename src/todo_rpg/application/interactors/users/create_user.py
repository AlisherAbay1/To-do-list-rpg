from todo_rpg.application.dto.common.users import CreateUserDTO, UserAuthDTO
from todo_rpg.application.exceptions import (
    EmailAlreadyTakenError,
    UsernameAlreadyTakenError,
)
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.repositories_interfaces import (
    UserRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol
from todo_rpg.core.security import hash_password
from todo_rpg.domain import User
from todo_rpg.application.mappers.common import UserMapper


class CreateUserInteractor:
    def __init__(
        self,
        repo: UserRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.uow = uow

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
        user_result = UserMapper.to_auth_dto(domain=user, session_token=session_token)

        await self.uow.commit()
        return user_result
