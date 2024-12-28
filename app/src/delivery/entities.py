from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class GetParcelsFilterParams(BaseModel):
    offset: int = 0
    limit: int = 100
    page_type: UUID | None = None
    with_delivery_price: bool | None = None


class RegisterParcelDTO(BaseModel):
    # idempotency key, remove default value in prod
    request_id: UUID = Field(default_factory=uuid4)

    weight: float = Field(1, ge=0)
    dollar_price: Decimal = Field(Decimal(1), ge=0)
    parcel_type_id: UUID
    name: str = ""
