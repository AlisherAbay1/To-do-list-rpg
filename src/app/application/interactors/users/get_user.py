from src.app.application.interfaces.repositories_interfaces import UserRepositoryProtocol

class GetUserInteractor:
    def __init__(self, repo: UserRepositoryProtocol) -> None:
        self.repo = repo

    async def __call__(self, user_id):
        user = await self.repo.get_user(user_id)
        return user