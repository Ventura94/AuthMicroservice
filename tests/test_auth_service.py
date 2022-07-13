from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from pytest_mock import MockerFixture

from schemas.user import UserO2Auth
from service_wrapper.orm.asyncio.mongodb import MongoDB
from tests.auth_fixtutes import *
from tools.email import Email


def test_authorized_exception(auth_service) -> None:
    result = auth_service.authorized_exception(message="Soy un error")
    assert result.status_code == 401
    assert result.detail == "Soy un error"


@pytest.mark.anyio
async def test_o2auth(mocker: MockerFixture, auth_service, false_token, user_dict_not_password, mongo_user) -> None:
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
    result = await auth_service.o2auth(false_token)
    assert result == UserO2Auth(**mongo_user)


@pytest.mark.anyio
async def test_o2auth(mocker: MockerFixture, auth_service, false_token, user_dict_not_password, mongo_user) -> None:
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
    result = await auth_service.o2auth(false_token)
    assert result == UserO2Auth(**mongo_user)


@pytest.mark.anyio
async def test_before_create(mocker: MockerFixture, auth_service, user_register_form) -> None:
    mocker.patch.object(
        Email,
        "is_valid",
        return_value=True,
        autospec=True,
    )
    mocker.patch.object(
        AuthService,
        "uniques_verify",
        return_value=None,
        autospec=True,
    )
    mocker.patch.object(
        CryptContext,
        "hash",
        return_value=false_hash_password,
        autospec=True,
    )
    result = await auth_service.before_create(**user_register_form)
    user_register_form["password"] = false_hash_password
    assert user_register_form == result


@pytest.mark.anyio
async def test_before_create_invalid_email(mocker: MockerFixture, auth_service, user_register_form) -> None:
    mocker.patch.object(
        Email,
        "is_valid",
        return_value=False,
        autospec=True,
    )
    mocker.patch.object(
        AuthService,
        "uniques_verify",
        return_value=None,
        autospec=True,
    )
    mocker.patch.object(
        CryptContext,
        "hash",
        return_value=false_hash_password,
        autospec=True,
    )

    with pytest.raises(HTTPException):
        await auth_service.before_create(**user_register_form)


@pytest.mark.anyio
async def test_user_authenticate(mocker: MockerFixture, auth_service, mongo_user, user_autenticate) -> None:
    mocker.patch.object(
        Email,
        "is_valid",
        return_value=False,
        autospec=True,
    )
    mocker.patch.object(
        MongoDB,
        "get",
        return_value=mongo_user,
        autospec=True,
    )
    mocker.patch.object(
        CryptContext,
        "verify",
        return_value=True,
        autospec=True,
    )
    result = await auth_service.user_authenticate(**user_autenticate)
    assert result == UserO2Auth(**mongo_user)


@pytest.mark.anyio
async def test_user_authenticate_with_user_deleted(mocker: MockerFixture, auth_service, mongo_user_deleted,
                                                   user_autenticate) -> None:
    mocker.patch.object(
        Email,
        "is_valid",
        return_value=False,
        autospec=True,
    )
    mocker.patch.object(
        MongoDB,
        "get",
        return_value=mongo_user_deleted,
        autospec=True,
    )
    mocker.patch.object(
        CryptContext,
        "verify",
        return_value=True,
        autospec=True,
    )
    with pytest.raises(HTTPException):
        await auth_service.user_authenticate(**user_autenticate)


@pytest.mark.anyio
async def test_user_authenticate_with_incorrect_password(mocker: MockerFixture, auth_service, mongo_user,
                                                         user_autenticate) -> None:
    mocker.patch.object(
        Email,
        "is_valid",
        return_value=False,
        autospec=True,
    )
    mocker.patch.object(
        MongoDB,
        "get",
        return_value=mongo_user,
        autospec=True,
    )
    mocker.patch.object(
        CryptContext,
        "verify",
        return_value=False,
        autospec=True,
    )
    with pytest.raises(HTTPException):
        await auth_service.user_authenticate(**user_autenticate)


@pytest.mark.anyio
async def test_before_update(mocker: MockerFixture, auth_service,
                             user_change_password_form) -> None:
    mocker.patch.object(
        CryptContext,
        "hash",
        return_value=false_hash_password,
        autospec=True,
    )
    result = await auth_service.before_update(**user_change_password_form)
    user_change_password_form["password"] = false_hash_password
    assert result == user_change_password_form


@pytest.mark.anyio
async def test_uniques_verify(mocker: MockerFixture, auth_service, user_register_form) -> None:
    mocker.patch.object(
        CryptContext,
        "hash",
        return_value=false_hash_password,
        autospec=True,
    )
    mocker.patch.object(
        AuthService,
        "is_exist_in_db",
        return_value=False,
        autospec=True,
    )
    assert await auth_service.uniques_verify(**user_register_form) is None


@pytest.mark.anyio
async def test_uniques_verify_not_uniques(mocker: MockerFixture, auth_service, user_register_form) -> None:
    mocker.patch.object(
        CryptContext,
        "hash",
        return_value=false_hash_password,
        autospec=True,
    )
    mocker.patch.object(
        AuthService,
        "is_exist_in_db",
        return_value=True,
        autospec=True,
    )
    with pytest.raises(HTTPException):
        await auth_service.uniques_verify(**user_register_form)


@pytest.mark.anyio
async def test_uniques_verify_not_uniques(mocker: MockerFixture, auth_service, user_register_form) -> None:
    mocker.patch.object(
        CryptContext,
        "hash",
        return_value=false_hash_password,
        autospec=True,
    )
    mocker.patch.object(
        AuthService,
        "is_exist_in_db",
        return_value=True,
        autospec=True,
    )
    with pytest.raises(HTTPException):
        await auth_service.uniques_verify(**user_register_form)


@pytest.mark.anyio
async def test_is_exist_in_db(mocker: MockerFixture, mongo_user, auth_service) -> None:
    mocker.patch.object(
        MongoDB,
        "get",
        return_value=mongo_user,
        autospec=True,
    )
    result = await auth_service.is_exist_in_db()
    assert result == True


@pytest.mark.anyio
async def test_is_exist_in_db_false(mocker: MockerFixture, auth_service) -> None:
    mocker.patch.object(
        MongoDB,
        "get",
        return_value=None,
        autospec=True,
    )
    result = await auth_service.is_exist_in_db()
    assert result == False
