import asyncio
from datetime import date, datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotel

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get("/{location}")
@cache(expire=30)
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
    date_to: date = Query(
        ..., description=f"Например, {(datetime.now() + timedelta(days=14)).date()}"
    ),
) -> list[SHotel]:
    # if date_from > date_to:
    # raise DateFromCannotBeAfterDateTo
    # if (date_to - date_from).days > 31:
    # raise CannotBookHotelForLongPeriod
    await asyncio.sleep(3)
    hotels = await HotelDAO.find_all(location, date_from, date_to)
    return hotels


@router.get("/id/{hotel_id}")
async def get_hotel_by_id(
    hotel_id: int,
) -> Optional[SHotel]:
    return await HotelDAO.find_by_id(model_id=hotel_id)
    # в файле return await HotelDAO.find_one_or_none(id=hotel_id)
