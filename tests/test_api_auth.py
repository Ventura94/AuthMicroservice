from httpx import AsyncClient
from jose import jwt
from pytest_mock import MockerFixture

from forms.credencial import UserUpdateForm
from main import app
from service_wrapper.orm.asyncio.mongodb import MongoDB
from tests.auth_fixtutes import *


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


@pytest.mark.anyio
async def test_update_profile(mocker: MockerFixture, user_update_form, data_clean, user_dict_not_password, mongo_user):
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
    mocker.patch.object(
        UserUpdateForm,
        "clean_data",
        return_value=data_clean,
        autospec=True,
    )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        data = user_update_form
        response = await ac.patch("/auth/update_profile", data=data,
                                  headers={"Content-Type": "application/x-www-form-urlencoded",
                                           "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Impvbmhkb2UiLCJuYW1lIjoiSm9uaCIsImxhc3RfbmFtZSI6IkRvZSIsImVtYWlsIjoiam9uaGRvZUBnbWFpbC5jb20iLCJwaG9uZSI6IjEyMzQ1Njc4Iiwicm9sZSI6WyJkZWZhdWx0Il0sImV4cCI6MTY1NzQyMDA2M30.uArE5Hio--AXc-6Krw13TvVWP-MJtghLxdYI78fZnA8"})
        assert response.status_code == 200
