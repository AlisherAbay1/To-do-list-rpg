from src.app.application.interfaces.repositories_interfaces import UserRepositoryProtocol

class GetAllUsersInteractor:
    def __init__(self, repo: UserRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, limit, offset):
        users = await self.repo.get_all_users(limit, offset)
        return users
