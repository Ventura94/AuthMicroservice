from pytest_mock import MockerFixture

from tests.auth_fixtutes import *
from tools.email import Email


@pytest.fixture
def email():
    return Email()


@pytest.fixture
def email_address():
    return "jonhdoe@gmail.com"


def test_email_is_valid(email, email_address):
    result = email.is_valid(email_address)
    assert result == True


def test_email_is_valid_invalid(email):
    result = email.is_valid("thisisnotemail")
    assert result == False


def test_is_email(mocker: MockerFixture, email, email_address):
    mocker.patch.object(
        Email,
        "is_valid",
        return_value=True,
        autospec=True,
    )
    result = email.is_email(email_address)
    assert result == True


def test_is_email_not_email(mocker: MockerFixture, email):
    mocker.patch.object(
        Email,
        "is_valid",
        return_value=False,
        autospec=True,
    )
    result = email.is_email("thisisnotemail")
    assert result == False
