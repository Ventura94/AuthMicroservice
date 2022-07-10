import pytest
from ServiceWrapper.orm.asyncio.mongodb import MongoDB
from bson import ObjectId
from httpx import AsyncClient
from pytest_mock.plugin import MockerFixture

from main import app
from services.auth_service import AuthService

"""
{'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Impvbmhkb2UiLCJuYW1lIjoiSm9uaCIsImxhc3RfbmFtZSI6IkRvZSIsImVtYWlsIjoiam9uaGRvZUBnbWFpbC5jb20iLCJwaG9uZSI6IjEyMzQ1Njc4Iiwicm9sZSI6WyJkZWZhdWx0Il0sImV4cCI6MTY1NzQyMDA2M30.uArE5Hio--AXc-6Krw13TvVWP-MJtghLxdYI78fZnA8', 'token_type': 'bearer'}

"""


@pytest.mark.anyio
async def test_login(mocker: MockerFixture) -> None:
    mocker.patch.object(
        MongoDB,
        "get",
        return_value={'_id': ObjectId('62ca30f510685b55dd844c1b'), 'username': 'jonhdoe', 'name': 'Jonh',
                      'last_name': 'Doe', 'email': 'jonhdoe@gmail.com', 'phone': '12345678',
                      'password': '$2b$12$bg8hu.SPK9t/rOOEzeKTl.mDGOkC.vCEIlNNR90Am0onoxKIOqOgG', 'role': ['default'],
                      'is_delete': False, 'delete_at': None},
        autospec=True,
    )
    async with AsyncClient(app=app, base_url="http://test") as ac:
        data = {"username": "johndoe", "password": "secret"}
        response = await ac.post("/auth/login", data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200


@pytest.mark.anyio
async def test_register(mocker: MockerFixture):
    mocker.patch.object(
        AuthService,
        "create",
        return_value=None,
        autospec=True,
    )
    async with AsyncClient(app=app, base_url="http://test") as ac:
        data = dict(
            username="johndoe",
            name="John",
            last_name="Doe",
            email="johndoe@gmail.com",
            phone="12345678",
            password="secret",
        )
        response = await ac.post("/auth/register", data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
        assert response.status_code == 200
