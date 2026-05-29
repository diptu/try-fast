from pydantic import BaseModel, Field


class AddressBase(BaseModel):
    street: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
    postal_code: str = Field(..., alias="postalCode", min_length=1)
    country: str = Field(..., min_length=1)

    is_default: bool = Field(default=False, alias="isDefault")

    model_config = {"populate_by_name": True}
