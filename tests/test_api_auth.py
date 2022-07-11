from typing import Dict, Optional, List, Union

import pytest
from bson import ObjectId
from httpx import AsyncClient
from jose import jwt
from pytest_mock import MockerFixture
from service_wrapper.orm.asyncio.mongodb import MongoDB

from main import app
from services.auth_service import AuthService


@pytest.fixture
def user_dict_not_password() -> Dict[str, Optional[Union[List[str], str]]]:
    return {"username": "johndoe",
            "name": "John",
            "last_name": "Doe",
            "email": "johndoe@gmail.com",
            "phone": "12345678",
            "role": ["default"]
            }


@pytest.fixture
def user_register_form() -> Dict[str, str]:
    return dict(
        username="johndoe",
        name="John",
        last_name="Doe",
        email="johndoe@gmail.com",
        phone="12345678",
        password="secret",
    )


@pytest.fixture
def user_change_password_form() -> Dict[str, str]:
    return {"password": "new_password"}


@pytest.fixture
def mongo_user() -> Dict[str, Optional[Union[ObjectId, str, bool]]]:
    return {'_id': ObjectId('62ca30f510685b55dd844c1b'), 'username': 'jonhdoe', 'name': 'Jonh',
            'last_name': 'Doe', 'email': 'jonhdoe@gmail.com', 'phone': '12345678',
            'password': '$2b$12$bg8hu.SPK9t/rOOEzeKTl.mDGOkC.vCEIlNNR90Am0onoxKIOqOgG', 'role': ['default'],
            'is_delete': False, 'delete_at': None}


@pytest.mark.anyio
async def test_login(mocker: MockerFixture, mongo_user) -> None:
    mocker.patch.object(
        MongoDB,
        "get",
        return_value=mongo_user,
        autospec=True,
    )
    async with AsyncClient(app=app, base_url="http://test") as ac:
        data = {"username": "johndoe", "password": "secret"}
        response = await ac.post("/auth/login", data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200


@pytest.mark.anyio
async def test_register_user(mocker: MockerFixture, user_register_form):
    mocker.patch.object(
        AuthService,
        "create",
        return_value=None,
        autospec=True,
    )
    async with AsyncClient(app=app, base_url="http://test") as ac:
        data = user_register_form
        response = await ac.post("/auth/register", data=data,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
        assert response.status_code == 200


@pytest.mark.anyio
async def test_delete_user(mocker: MockerFixture, mongo_user, user_dict_not_password):
    mocker.patch.object(
        AuthService,
        "o2auth",
        return_value=user_dict_not_password,
        autospec=True,
    )
    mocker.patch.object(
        jwt,
        "decode",
        return_value=user_dict_not_password,
        autospec=True,
    )
    mocker.patch.object(
        MongoDB,
        "get",
        return_value=mongo_user,
        autospec=True,
    )
    mocker.patch.object(
        AuthService,
        "delete",
        return_value=None,
        autospec=True,
    )
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/auth/delete_user",
                                   headers={"Content-Type": "application/json",
                                            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Impvbmhkb2UiLCJuYW1lIjoiSm9uaCIsImxhc3RfbmFtZSI6IkRvZSIsImVtYWlsIjoiam9uaGRvZUBnbWFpbC5jb20iLCJwaG9uZSI6IjEyMzQ1Njc4Iiwicm9sZSI6WyJkZWZhdWx0Il0sImV4cCI6MTY1NzQyMDA2M30.uArE5Hio--AXc-6Krw13TvVWP-MJtghLxdYI78fZnA8"})
        assert response.status_code == 200


@pytest.mark.anyio
async def test_change_password(mocker: MockerFixture, mongo_user, user_dict_not_password, user_change_password_form):
    mocker.patch.object(
        AuthService,
        "o2auth",
        return_value=user_dict_not_password,
        autospec=True,
    )
    mocker.patch.object(
        jwt,
        "decode",
        return_value=user_dict_not_password,
        autospec=True,
    )
    mocker.patch.object(
        MongoDB,
        "get",
        return_value=mongo_user,
        autospec=True,
    )
    mocker.patch.object(
        AuthService,
        "update",
        return_value=None,
        autospec=True,
    )
    data = user_change_password_form
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.patch("/auth/change_password", data=data,
                                  headers={"Content-Type": "application/x-www-form-urlencoded",
                                           "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Impvbmhkb2UiLCJuYW1lIjoiSm9uaCIsImxhc3RfbmFtZSI6IkRvZSIsImVtYWlsIjoiam9uaGRvZUBnbWFpbC5jb20iLCJwaG9uZSI6IjEyMzQ1Njc4Iiwicm9sZSI6WyJkZWZhdWx0Il0sImV4cCI6MTY1NzQyMDA2M30.uArE5Hio--AXc-6Krw13TvVWP-MJtghLxdYI78fZnA8"})
        assert response.status_code == 200
