from fastapi import APIRouter, HTTPException, Depends, Form
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
        200: {"description": "User was successfully registered."},
        400: {"description": "Validation error (e.g., passwords mismatch or email already registered)."},
        500: {"description": "Unexpected error during registration."},
    },
)
async def register_user(user: UserCreate) -> dict:
    """
    Регистрация нового пользователя (E-mail уникален).

    Args:
        user (UserCreate): Данные создаваемого пользователя.

    Returns:
        dict: Сообщение об успешной регистрации.

    Raises:
        HTTPException: Если пароли не совпадают или возникли другие ошибки.
    """
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    try:
        return await register_user_crud(user)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
    except Exception:
        print(f"Unexpected error during registration: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Unexpected error during registration")


@router.post(
    "/login",
    responses={
        200: {"description": "User authenticated successfully. JWT token returned."},
        401: {"description": "Invalid credentials provided."},
        500: {"description": "Unexpected error during login."},
    },
)
async def login_user(
        username: str = Form(..., description="User's email"),  # Используем Form для обработки form-data
        password: str = Form(..., description="User's password"),
        grant_type: str = Form(default="password", description="OAuth2 grant type, default is 'password'"),
) -> dict:
    """
    Аутентификация пользователя с использованием OAuth2 формата (username вместо email).

    Args:
        username (str): E-mail пользователя.
        password (str): Пароль пользователя.
        grant_type (str): Тип гранта для OAuth2 (по умолчанию "password").

    Returns:
        dict: Токен доступа в случае успешного входа.

    Raises:
        HTTPException: Если учетные данные некорректны или произошла другая ошибка.
    """
    try:
        # Используем username как email
        user_data = UserLogin(email=username, password=password)
        return await login_user_crud(user_data)
    except ValueError as ve:
        raise HTTPException(status_code=401, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
    except Exception:
        print(f"Unexpected error during login: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Unexpected error during login")


@router.get(
    "/protected",
    responses={
        200: {"description": "Access granted to the protected route."},
        401: {"description": "Invalid or expired JWT token."},
        500: {"description": "Unexpected error during token verification."},
    },
)
async def protected_route(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Защищенный маршрут, требует валидного токена.

    Args:
        token (str): JWT-токен пользователя, переданный через заголовок.

    Returns:
        dict: Приветственное сообщение для пользователя.

    Raises:
        HTTPException: Если токен недействителен, истек или произошла другая ошибка.
    """
    try:
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        return {"msg": f"Hello, {payload.get('sub')}!"}
    except HTTPException as he:
        raise he
    except Exception:
        print(f"Unexpected error during token decoding: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred during token verification")
