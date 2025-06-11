from pydantic_settings import BaseModel, Field, HttpUrl, PositiveFloat
from pydantic import BaseModel, Field, HttpUrl, PositiveFloat
from uuid import UUID, uuid4
from datetime import date

class Offer(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="Unique identifier for the offer")
    url: HttpUrl = Field(..., description="URL to the offer listing")
    title: str = Field(..., min_length=1, max_length=255, description="Title of the offer")
    price: PositiveFloat = Field(..., description="Price of the offer")
    price_per_meter: PositiveFloat = Field(..., alias="price_per_meter", description="Price per square meter")
    area: PositiveFloat = Field(..., description="Total area in square meters")
    source: str = Field(..., min_length=1, description="Source website or platform")
    found_date: date = Field(..., description="Date when the offer was found")
    favourite: bool = Field(default=False, description="Flag if the offer is marked as favourite")
    hidden: bool = Field(default=False, description="Flag if the offer is hidden from listing")

    class Config:
        allow_population_by_field_name = True
        anystr_strip_whitespace = True
        orm_mode = True
