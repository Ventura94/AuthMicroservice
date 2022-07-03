from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from forms.credencial import UserRegisterForm, UserCredentialsForm
from schemas.token import Token
from schemas.user import User, UserInBD
from services.auth_service import AuthService
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/auth", tags=["authorization"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", description="authorization")


@router.post(
    "/login",
    response_model=Token,
    name="Login System",
    description="Credentials are sent to build the access token",
)
async def login(form_data: UserCredentialsForm = Depends()):
    try:
        user = await AuthService().user_authenticate(
            form_data.username, form_data.password
        )
        token_data = user.dict()
        access_token_expires = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        token_data.update({"exp": access_token_expires})
        encoded_jwt = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": encoded_jwt, "token_type": "bearer"}
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/users/register")
async def register(form_data: UserRegisterForm = Depends()):
    data = dict(
        username=form_data.username,
        name=form_data.name,
        last_name=form_data.last_name,
        email=form_data.email,
        phone=form_data.phone,
        password=form_data.password,
        is_active=True,
        role=[
            "default",
        ],
    )
    try:
        await AuthService().create(**UserInBD(**data).dict())
        return User(**data)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/auth_user/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
