from src.app.application.interfaces.repositories_interfaces import \
    UserRepositoryProtocol
from src.app.application.mappers import UserMapper
from src.app.application.dto.users import UserDTO

class GetAllUsersInteractor:
    def __init__(self, repo: UserRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, limit, offset) -> list[UserDTO]:
        users = await self.repo.get_all_users(limit, offset)
        dtos = UserMapper.to_list_dto(users)
        return dtos
