from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.utils.number_utils import only_numbers


class AddressResponse(BaseModel):
    zipcode: Optional[str] = Field(None)
    street: Optional[str] = Field(None)
    complement: Optional[str] = Field(None)
    unit: Optional[str] = Field(None)
    neighborhood: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    state_code: Optional[str] = Field(None)
    state: Optional[str] = Field(None)
    region: Optional[str] = Field(None)

    @field_validator("zipcode")
    @classmethod
    def sync_zipcode(cls, value: Optional[str]) -> Optional[str]:
        if value:
            return only_numbers(value)
