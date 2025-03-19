import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("kot@pes.com", "kotopes", 201),
        ("kot@pes.com", "kot0pes", 409),
        ("pes@kot.com", "pesokot", 201),
        ("abcd", "glhf", 422),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/register/",
        json={
            "email": email,  # Используем переданный параметр
            "password": password,  # Используем переданный параметр
        },
        follow_redirects=True,
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("test@test.com", "test", 200),
        ("artem@example.com", "artem", 200),
        ("wrong@person.com", "artem", 401),
    ],
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
        follow_redirects=True,
    )

    assert response.status_code == status_code
