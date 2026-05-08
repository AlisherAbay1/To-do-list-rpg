from typing import Optional, Sequence
from uuid import UUID
from src.app.domain import Shop
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

class ShopRepository:
    __slots__ = ("_session", )
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def get_shop_listings_by_user_id(self, user_id: UUID, limit: int, offset: int) -> Sequence[Shop]: 
        shop_listings = select(Shop).where(Shop.user_id == user_id).limit(limit).offset(offset)
        result = await self._session.scalars(shop_listings)
        return result.all()
    
    async def get_shop_listing_by_id(self, shop_listing_id: UUID) -> Optional[Shop]:
        shop_listing = select(Shop).where(Shop.id == shop_listing_id).with_for_update()
        result = await self._session.scalar(shop_listing)
        return result
    
    async def get_shop_listing_by_item_id(self, item_id: UUID) -> Optional[Shop]:
        shop_listing = select(Shop).where(Shop.item_id == item_id).with_for_update()
        result = await self._session.scalar(shop_listing)
        return result
    
    async def delete(self, shop_listing: Shop) -> None: 
        await self._session.delete(shop_listing)