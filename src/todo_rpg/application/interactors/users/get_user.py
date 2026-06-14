from todo_rpg.application.mappers.common import UserMapper
from todo_rpg.application.exceptions import UserNotFoundError
from todo_rpg.application.interfaces.repositories_interfaces import (
    UserRepositoryProtocol,
)
from todo_rpg.application.dto import UserDTO


class GetUserInteractor:
    def __init__(self, repo: UserRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, user_id) -> UserDTO:
        user = await self.repo.get_user(user_id)
        if user is None:
            raise UserNotFoundError()
        return UserMapper.to_dto(user)
