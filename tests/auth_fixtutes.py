import pytest
from bson import ObjectId

from forms.credencial import UserUpdateForm
from services.auth_service import AuthService


@pytest.fixture
def user_update_form_class():
    return UserUpdateForm(username="johndoe",
                          name=None,
                          last_name=None,
                          email=None,
                          phone=None,
                          )


@pytest.fixture
def auth_service():
    return AuthService()


@pytest.fixture
def false_hash_password():
    return '$2b$12$bg8hu.SPK9t/rOOEzeKTl.mDGOkC.vCEIlNNR90Am0onoxKIOqOgG'


@pytest.fixture
def false_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Impvbmhkb2UiLCJuYW1lIjoiSm9uaCIsImxhc3RfbmFtZSI6IkRvZSIsImVtYWlsIjoiam9uaGRvZUBnbWFpbC5jb20iLCJwaG9uZSI6IjEyMzQ1Njc4Iiwicm9sZSI6WyJkZWZhdWx0Il0sImV4cCI6MTY1NzQyMDA2M30.uArE5Hio--AXc-6Krw13TvVWP-MJtghLxdYI78fZnA8"


@pytest.fixture
def data_clean():
    return {"user_id": 'jonhdoe12',
            "username": "johndoe", }


@pytest.fixture
def user_dict_not_password():
    return {"user_id": 'jonhdoe12',
            "username": "johndoe",
            "name": "John",
            "last_name": "Doe",
            "email": "johndoe@gmail.com",
            "phone": "12345678",
            "role": ["default"]
            }


@pytest.fixture
def user_register_form():
    return dict(
        username="johndoe",
        name="John",
        last_name="Doe",
        email="johndoe@gmail.com",
        phone="12345678",
        password="secret",
    )


@pytest.fixture
def user_update_form():
    return dict(
        username="john94",
        name=None,
        last_name=None,
        email=None,
        phone=None,
    )


@pytest.fixture
def user_change_password_form():
    return {"user_id": 'jonhdoe12', "password": "new_password"}


@pytest.fixture
def user_autenticate():
    return {"username": 'jonhdoe', "password": "secret"}


@pytest.fixture
def mongo_user():
    return {'_id': ObjectId('62ca30f510685b55dd844c1b'), "user_id": 'jonhdoe12', 'username': 'jonhdoe', 'name': 'Jonh',
            'last_name': 'Doe', 'email': 'jonhdoe@gmail.com', 'phone': '12345678',
            'password': '$2b$12$bg8hu.SPK9t/rOOEzeKTl.mDGOkC.vCEIlNNR90Am0onoxKIOqOgG', 'role': ['default'],
            'is_delete': False, 'delete_at': None}


@pytest.fixture
def mongo_user_deleted():
    return {'_id': ObjectId('62ca30f510685b55dd844c1b'), "user_id": 'jonhdoe12', 'username': 'jonhdoe', 'name': 'Jonh',
            'last_name': 'Doe', 'email': 'jonhdoe@gmail.com', 'phone': '12345678',
            'password': '$2b$12$bg8hu.SPK9t/rOOEzeKTl.mDGOkC.vCEIlNNR90Am0onoxKIOqOgG', 'role': ['default'],
            'is_delete': True, 'delete_at': None}
