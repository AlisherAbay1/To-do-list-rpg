from pydantic import BaseModel, Field, model_validator, field_validator, AwareDatetime
from datetime import datetime, timezone
from uuid import UUID


class ShopTransactionSchemaRead(BaseModel):
    id: UUID
    user_id: UUID
    shop_listing_id: UUID | None
    item_id: UUID | None
    item_title: str
    price: int
    date: datetime


class ShopTransactionFilters(BaseModel):
    date_from: AwareDatetime | None = None
    date_to: AwareDatetime | None = None
    sum_from: int | None = Field(default=None, gt=0)
    sum_to: int | None = Field(default=None, gt=0)

    @field_validator("date_from", "date_to", mode="after")
    @classmethod
    def transform_data_to_utc(cls, v: AwareDatetime | None):
        if v is not None:
            return v.astimezone(tz=timezone.utc)
        return v

    @model_validator(mode="after")
    def check_if_date_to_greater_than_date_from(self):
        if self.date_from is not None and self.date_to is not None:
            if self.date_from > self.date_to:
                raise ValueError("Date to should be greater than date from")
        return self

    @model_validator(mode="after")
    def check_if_sum_to_greater_than_sum_from(self):
        if self.sum_from is not None and self.sum_to is not None:
            if self.sum_from > self.sum_to:
                raise ValueError("Sum to should be greater than sum from")
        return self
