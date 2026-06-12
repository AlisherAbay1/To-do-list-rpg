from todo_rpg.application.interfaces.repositories_interfaces import (
    UserRepositoryProtocol,
)
from todo_rpg.application.mappers.common import UserMapper
from todo_rpg.application.dto.common.users import UserDTO


class GetAllUsersInteractor:
    def __init__(self, repo: UserRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, limit, offset) -> list[UserDTO]:
        users = await self.repo.get_all_users(limit, offset)
        dtos = UserMapper.to_list_dto(users)
        return dtos
