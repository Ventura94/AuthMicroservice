from fastapi import Form


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
