from fastapi import APIRouter, HTTPException, Depends
from crud.auth_crud import register_user_crud, login_user_crud
from models.user import UserCreate, UserLogin
from security.jwt import decode_access_token
from fastapi.security import OAuth2PasswordBearer
import traceback

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post(
    "/register",
    responses={
        200: {"description": "User was successfully registered"},
        400: {"description": "Validation error (e.g., passwords mismatch or email already registered)"},
        500: {"description": "Unexpected error during registration"},
    },
)
async def register_user(user: UserCreate):
    """
    Регистрация нового пользователя (E-mail уникален).
    """
    # Проверка совпадения паролей
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    try:
        return await register_user_crud(user)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        # Для ошибок базы данных или неожиданных
        raise HTTPException(status_code=500, detail=str(re))
    except Exception as e:
        print(f"Unexpected error during registration: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Unexpected error during registration")


@router.post(
    "/login",
    responses={
        200: {"description": "User authenticated successfully. JWT token returned."},
        401: {"description": "Invalid credentials provided"},
        500: {"description": "Unexpected error during login"},
    },
)
async def login_user(user: UserLogin):
    """
    Аутентификация пользователя. Возвращает JWT в случае успеха.
    """
    try:
        return await login_user_crud(user)
    except ValueError as ve:
        # Ошибки проверки учетных данных
        raise HTTPException(status_code=401, detail=str(ve))
    except RuntimeError as re:
        # Ошибки базы или другие неожиданные ошибки
        raise HTTPException(status_code=500, detail=str(re))
    except Exception as e:
        print(f"Unexpected error during login: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Unexpected error during login")


@router.get(
    "/protected",
    responses={
        200: {"description": "Access granted to the protected route"},
        401: {"description": "Invalid or expired JWT token"},
        500: {"description": "Unexpected error during token verification"},
    },
)
async def protected_route(token: str = Depends(oauth2_scheme)):
    """
    Защищенный маршрут, требующий валидного токена.
    """
    try:
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return {"msg": f"Hello, {payload.get('sub')}!"}
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Unexpected error during token decoding: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred during token verification")
