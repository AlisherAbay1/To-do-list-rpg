from todo_rpg.application.interfaces import (
    ShopRepositoryProtocol,
    SessionRepositoryProtocol,
    UoWProtocol,
)
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    ShopListingNotFoundError,
    AccessDeniedError,
)
from uuid import UUID


class DeleteCurrentUserShopListingInteractor:
    def __init__(
        self,
        repo: ShopRepositoryProtocol,
        session_repo: SessionRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.repo = repo
        self.session_repo = session_repo
        self.uow = uow

    async def __call__(self, shop_listing_id: UUID, session_token: str) -> None:
        user_id = await self.session_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()

        shop_listing = await self.repo.get_shop_listing_by_id(shop_listing_id)
        if shop_listing is None:
            raise ShopListingNotFoundError()
        if shop_listing.user_id != user_id:
            raise AccessDeniedError()

        await self.repo.delete(shop_listing)
        await self.uow.commit()
