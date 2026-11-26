from todo_rpg.application.interfaces import (
    UserRepositoryProtocol,
    SessionRepositoryProtocol,
)
from todo_rpg.application.mappers.common import UserMapper
from todo_rpg.application.dto.common.users import UserDTO
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    UserNotFoundError,
    AccessDeniedError,
)


class GetAllUsersInteractor:
    def __init__(
        self, repo: UserRepositoryProtocol, session_repo: SessionRepositoryProtocol
    ) -> None:
        self.repo = repo
        self.session_repo = session_repo

    async def __call__(
        self, session_token: str, limit: int, offset: int
    ) -> list[UserDTO]:
        user_id = await self.session_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        user = await self.repo.get_user(user_id)
        if user is None:
            raise UserNotFoundError()
        if not user.is_admin:
            raise AccessDeniedError()
        users = await self.repo.get_all_users(limit, offset)
        dtos = UserMapper.to_list_dto(users)
        return dtos
