import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id,date_from,date_to,status_code",
    [
        *[(4, "2030-05-01", "2030-05-15", 201)] * 8,
        (4, "2030-05-09", "2030-05-23", 409),
        (4, "2030-05-10", "2030-05-24", 409),
    ],
)
@pytest.mark.asyncio
async def test_add_and_get_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    authentificated_ac: AsyncClient,
):
    response = await authentificated_ac.post(
        "/bookings",
        params={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
        follow_redirects=True,
    )

    assert response.status_code == status_code

    assert response.json()
