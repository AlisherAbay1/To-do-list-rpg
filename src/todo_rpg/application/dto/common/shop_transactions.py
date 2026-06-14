from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class ShopTransactionDTO:
    id: UUID
    user_id: UUID
    shop_listing_id: UUID | None
    item_id: UUID | None
    item_title: str
    price: int
    date: datetime


@dataclass
class ShopTransactionFiltersDTO:
    date_from: datetime | None
    date_to: datetime | None
    sum_from: int | None
    sum_to: int | None
