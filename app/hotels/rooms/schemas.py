from typing import Optional

from pydantic import BaseModel, ConfigDict


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str]
    price: int
    services: list[str]  # == JSON
    quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)

    # class Config:
    # from_attributes = True
