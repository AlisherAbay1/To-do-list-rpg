from src.app.application.interfaces.transaction_interfaces import TransactionProtocol
from src.app.application.interfaces.cash_interfaces import RedisRepositoryProtocol
from src.app.application.mappers import ShopMapper
from src.app.application.dto import ShopListingShortDTO, ShopListingCreateDTO
from src.app.application.exceptions import SessionNotFoundError
from src.app.domain import Shop

class CreateCurrentUserShopListingInteractor:
    def __init__(self, 
                 cash_repo: RedisRepositoryProtocol, 
                 transaction: TransactionProtocol) -> None:
        self.cash_repo = cash_repo
        self.transaction = transaction

    async def __call__(self, session_token: str, dto: ShopListingCreateDTO) -> ShopListingShortDTO:
        user_id = await self.cash_repo.get_user_id_by_session_token(session_token)
        if user_id is None:
            raise SessionNotFoundError()
        shop_listing = Shop(
            user_id=user_id, 
            item_id=dto.item_id, 
            price=dto.price, 
            quantity=dto.quantity
        )
        await self.transaction.save(shop_listing)
        output_dto = ShopMapper.to_short_dto(shop_listing)
        await self.transaction.commit()
        return output_dto