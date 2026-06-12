from todo_rpg.application.dto.common.users import UserPasswordDTO
from todo_rpg.application.exceptions import (
    IncorrectPasswordError,
    SessionNotFoundError,
    UserNotFoundError,
)
from todo_rpg.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from todo_rpg.application.interfaces.repositories_interfaces import (
    UserRepositoryProtocol,
)
from todo_rpg.application.interfaces.transaction_interfaces import UoWProtocol
from todo_rpg.core.security import hash_password, password_verify


class UpdateCurrentUserPasswordInteractor:
    def __init__(
        self,
        repo: UserRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(self, dto: UserPasswordDTO, session_token: str):
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.repo.get_user(user_id)
        if not user:
            raise UserNotFoundError()
        if not password_verify(dto.old_password, user.password):
            raise IncorrectPasswordError()
        user.password = hash_password(dto.new_password)
        await self.uow.commit()
