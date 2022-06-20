from fastapi import APIRouter, Depends, HTTPException, status
from schemas.tocken import Token
from schemas.user import User, UserInBD
from forms.credencial import UserCredentialsForm, UserRegisterForm
from services.auth_service import AuthService
from utils.auth_tools import UserVerify, TokenTools, PasswordTools

# from database.queryset import UserMongoDB

router = APIRouter(prefix="/auth", tags=["authorization"])


# @router.post("/login",
#              response_model=Token,
#              name="Login System",
#              description="Credentials are sent to build the access token"
#              )
# async def login(form_data: UserCredentialsForm = Depends()):
#     try:
#         user = await UserVerify.user_authenticate(UserMongoDB(), form_data.username, form_data.password)
#         access_token = TokenTools.encode_token(user.dict())
#         return {"access_token": access_token, "token_type": "bearer"}
#     except ValueError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#

@router.post("/users/register")
async def register(
        # form_data: UserRegisterForm = Depends()
):
    # data = dict(
    #     username=form_data.username,
    #     name=form_data.name,
    #     last_name=form_data.last_name,
    #     email=form_data.email,
    #     phone=form_data.phone,
    #     password=PasswordTools.get_password_hash(form_data.password),
    #     is_active=True
    # )
    try:
        await AuthService.create(**{
            "username": "ventura94",
            "name": "Arian",
            "last_name": "Ventura Rodriguez",
            "email": "arianventura94@gmail.com",
            "phone": 53363930,
            "password": "arianvr191194",
            "is_active": True
        })
        # return User(**data)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
