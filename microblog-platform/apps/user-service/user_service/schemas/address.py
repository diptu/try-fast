from __future__ import annotations

from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

LabelField = Annotated[
    str,
    Field(
        min_length=1,
        max_length=50,
        examples=["Home"],
    ),
]

StreetField = Annotated[
    str,
    Field(
        max_length=255,
        examples=["House 12, Road 5"],
    ),
]

CityField = Annotated[
    str,
    Field(
        max_length=100,
        examples=["Dhaka"],
    ),
]

StateField = Annotated[
    str,
    Field(
        max_length=100,
        examples=["Dhaka"],
    ),
]

PostalCodeField = Annotated[
    str,
    Field(
        max_length=20,
        examples=["1216"],
    ),
]

CountryField = Annotated[
    str,
    Field(
        max_length=100,
        examples=["Bangladesh"],
    ),
]


class AddressBase(BaseModel):
    """
    Shared address fields.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    label: LabelField
    street: StreetField
    city: CityField
    state: StateField
    postal_code: PostalCodeField
    country: CountryField


class AddressCreate(AddressBase):
    """
    Request schema for creating an address.
    """

    is_default: bool = False


class AddressUpdate(BaseModel):
    """
    Request schema for partially updating an address.
    """

    model_config = ConfigDict(
        extra="forbid",
    )

    label: LabelField | None = None
    street: StreetField | None = None
    city: CityField | None = None
    state: StateField | None = None
    postal_code: PostalCodeField | None = None
    country: CountryField | None = None

    is_default: bool | None = None


class AddressResponse(AddressBase):
    """
    Address response schema.
    """

    id: UUID
    user_id: UUID

    is_default: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


class AddressListResponse(BaseModel):
    """
    Response schema for listing addresses.
    """

    items: list[AddressResponse]
