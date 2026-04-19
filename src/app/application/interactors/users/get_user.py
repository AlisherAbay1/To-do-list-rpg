from src.app.application.interfaces.repositories_interfaces import UserRepositoryProtocol
from src.app.application.dto_mappers import UserMapper
from src.app.application.exceptions import UserNotFoundError

class GetUserInteractor:
    def __init__(self, repo: UserRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, user_id):
        user = await self.repo.get_user(user_id)
        if user is None:
            raise UserNotFoundError()
        return UserMapper.to_dto(user)