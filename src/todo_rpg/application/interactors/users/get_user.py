from todo_rpg.application.mappers.common import UserMapper
from todo_rpg.application.interfaces import (
    UserRepositoryProtocol,
)
from todo_rpg.application.dto import UserDTO
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    UserNotFoundError,
    AccessDeniedError,
    TargetUserNotFoundError,
)


class GetUserInteractor:
    def __init__(self, repo: UserRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, session_token: str, target_user_id: str) -> UserDTO:
        current_user_id = await self.session_repo.get_user_id_by_session_token(
            session_token
        )
        if current_user_id is None:
            raise SessionNotFoundError()
        current_user = await self.user_repo.get_user(current_user_id)
        if current_user is None:
            raise UserNotFoundError()
        if not current_user.is_admin:
            raise AccessDeniedError()
        target_user = await self.repo.get_user(target_user_id)
        if target_user is None:
            raise TargetUserNotFoundError()
        return UserMapper.to_dto(target_user)
