from inspect import signature
from typing import Union, Dict

from fastapi import Form


class ChangePasswordForm:
    def __init__(self, password: str = Form(...)):
        self.password = password


class UserCredentialsForm:
    def __init__(
            self,
            username: str = Form(...),
            password: str = Form(...),
    ):
        self.username = username
        self.password = password


class UserRegisterForm:
    def __init__(
            self,
            username: str = Form(...),
            name: str = Form(...),
            last_name: str = Form(...),
            email: str = Form(...),
            phone: str = Form(...),
            password: str = Form(...),
    ):
        self.username = username
        self.name = name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.password = password


class UserUpdateForm:
    def __init__(
            self,
            username: str = Form(default=None),
            name: str = Form(default=None),
            last_name: str = Form(default=None),
            email: str = Form(default=None),
            phone: str = Form(default=None),

    ):
        self.username = username
        self.name = name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    def clean_data(self, **kwargs) -> Dict[str, Union[str, float, int]]:
        data = {}
        for field in signature(self.__class__).parameters:
            if getattr(self, field) is None:
                del kwargs[field]
            else:
                data[field] = getattr(self, field)
        kwargs.update(data)
        return kwargs
