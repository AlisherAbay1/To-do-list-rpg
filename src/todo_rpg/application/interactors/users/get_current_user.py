from todo_rpg.application.mappers.common import UserMapper
from todo_rpg.application.exceptions import SessionNotFoundError, UserNotFoundError
from todo_rpg.application.interfaces import (
    UserRepositoryProtocol,
    RedisRepositoryProtocol,
)
from todo_rpg.application.dto import UserDTO


class GetCurrentUser:
    def __init__(
        self, repo: UserRepositoryProtocol, cash_repo: RedisRepositoryProtocol
    ) -> None:
        self.repo = repo
        self.cash_repo = cash_repo

    async def __call__(self, session_token) -> UserDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.repo.get_user(user_id)
        if user is None:
            raise UserNotFoundError()
        return UserMapper.to_dto(user)
