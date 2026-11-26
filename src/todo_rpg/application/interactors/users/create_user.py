from todo_rpg.application.dto.common.users import CreateUserDTO, UserAuthDTO
from todo_rpg.domain.exceptions import (
    EmailAlreadyTakenError,
    UsernameAlreadyTakenError,
)
from todo_rpg.application.interfaces import (
    SessionRepositoryProtocol,
    UserRepositoryProtocol,
    PasswordManagerProtocol,
    UoWProtocol,
)
from todo_rpg.domain import User
from todo_rpg.application.mappers.common import UserMapper


class CreateUserInteractor:
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

    async def __call__(self, dto: CreateUserDTO) -> UserAuthDTO:
        if await self.repo.is_username_taken(dto.username):
            raise UsernameAlreadyTakenError()
        if await self.repo.is_email_taken(dto.email):
            raise EmailAlreadyTakenError()
        hashed_password = self.password_manager.hash_password(dto.password)
        user = User(
            username=dto.username,
            email=dto.email,
            password=hashed_password,
        )
        self.repo.save(user)

        session_token = await self.session_repo.create_session(str(user.id))
        user_result = UserMapper.to_auth_dto(domain=user, session_token=session_token)

        await self.uow.commit()
        return user_result
