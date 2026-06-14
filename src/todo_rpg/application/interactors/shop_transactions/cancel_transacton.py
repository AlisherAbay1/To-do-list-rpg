from todo_rpg.application.interfaces import (
    RedisRepositoryProtocol,
    ShopTransactionRepositoryProtocol,
    InventoryRepositoryProtocol,
    ShopRepositoryProtocol,
    UserRepositoryProtocol,
    UoWProtocol,
)
from todo_rpg.application.exceptions import (
    SessionNotFoundError,
    ShopTransactionNotFoundError,
    ShopListingNotFoundError,
    InventoryItemNotFoundError,
    UserNotFoundError,
    AccessDeniedError,
)
from uuid import UUID


class CancelTransactionInteractor:
    def __init__(
        self,
        shop_transaction_repo: ShopTransactionRepositoryProtocol,
        inventory_repo: InventoryRepositoryProtocol,
        shop_repo: ShopRepositoryProtocol,
        user_repo: UserRepositoryProtocol,
        cash_repo: RedisRepositoryProtocol,
        uow: UoWProtocol,
    ) -> None:
        self.shop_transaction_repo = shop_transaction_repo
        self.inventory_repo = inventory_repo
        self.shop_repo = shop_repo
        self.user_repo = user_repo
        self.cash_repo = cash_repo
        self.uow = uow

    async def __call__(self, session_token: str, shop_transaction_id: UUID) -> None:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        shop_transaction = await self.shop_transaction_repo.get_shop_transaction_by_id(
            shop_transaction_id
        )
        if shop_transaction is None:
            raise ShopTransactionNotFoundError()
        if shop_transaction.user_id != user_id:
            raise AccessDeniedError()
        user = await self.user_repo.get_user(user_id)
        if user is None:
            raise UserNotFoundError()
        if shop_transaction.shop_listing_id:
            shop_listing = await self.shop_repo.get_shop_listing_by_id(
                shop_transaction.shop_listing_id
            )

            if shop_listing is None:
                raise ShopListingNotFoundError()

            if shop_transaction.item_id is not None:
                inventory = await self.inventory_repo.get_inventory_item_by_item_id(
                    shop_transaction.item_id, user_id
                )
                if inventory is None:
                    raise InventoryItemNotFoundError()
                if inventory.quantity > 0:
                    inventory.quantity -= 1
                    user.gold += shop_transaction.price

            shop_listing.quantity += 1

        elif shop_transaction.item_id:
            raise ShopListingNotFoundError()

        await self.uow.delete(shop_transaction)
        await self.uow.commit()
