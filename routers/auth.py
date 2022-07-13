import random
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from forms.credencial import UserRegisterForm, UserCredentialsForm, ChangePasswordForm, UserUpdateForm
from schemas.token import Token
from schemas.user import User, UserInBD, UserO2Auth
from services.auth_service import AuthService
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY

router = APIRouter(prefix="/auth", tags=["Authorization"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", description="authorization")


@router.post(
    "/login",
    response_model=Token,
    name="Login user authentication",
    description="Credentials are sent to build the access token",
)
async def login(form_data: UserCredentialsForm = Depends()):
    user = await AuthService().user_authenticate(
        form_data.username, form_data.password
    )
    token_data = user.dict()
    access_token_expires = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token_data.update({"exp": access_token_expires})
    encoded_jwt = jwt.encode(token_data, SECRET_KEY)
    return {"access_token": encoded_jwt, "token_type": "bearer"}


@router.post("/register",
             response_model=User,
             name="Register users",
             description="Register users")
async def register(form_data: UserRegisterForm = Depends()):
    data = dict(
        user_id=f"{form_data.username}{random.randint(0, 100)}",
        username=form_data.username,
        name=form_data.name,
        last_name=form_data.last_name,
        email=form_data.email,
        phone=form_data.phone,
        password=form_data.password,
        is_delete=False,
        role=[
            "default",
        ],
    )
    await AuthService().create(**UserInBD(**data).dict())
    return User(**data)


@router.get("/auth_user",
            response_model=User,
            name="Authenticate user data",
            description="Get authenticate user data")
async def auth_user(user: User = Depends(AuthService().o2auth)):
    return user


@router.patch("/update_profile")
async def update_profile(user: UserO2Auth = Depends(AuthService().o2auth),
                         user_profile_form: UserUpdateForm = Depends()):
    data_to_update = user_profile_form.clean_data(**user.dict())
    await AuthService().update(by="user_id", **data_to_update)
    return {"detail": "Profile has changed"}


@router.patch("/change_password")
async def change_password(user: UserO2Auth = Depends(AuthService().o2auth),
                          password_form: ChangePasswordForm = Depends()):
    await AuthService().update(by="user_id", user_id=user.user_id, password=password_form.password)
    return {"detail": "Password has changed"}


@router.delete("/delete_user")
async def delete_user(user: UserO2Auth = Depends(AuthService().o2auth)):
    await AuthService().delete(by="user_id", **user.dict())
    return {"detail": "User deleted successfully"}
