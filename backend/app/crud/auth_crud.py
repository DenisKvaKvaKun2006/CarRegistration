from pymongo.errors import PyMongoError
from database import users_collection
from models.user import UserCreate, UserLogin
from security.hashing import hash_password, verify_password
from security.jwt import create_access_token
from typing import Dict


async def register_user_crud(user: UserCreate) -> Dict[str, str]:
    """
    Регистрация нового пользователя.

    E-mail должен быть уникальным в базе данных.

    Args:
        user (UserCreate): Данные нового пользователя.

    Returns:
        Dict[str, str]: Сообщение о статусе операции.

    Raises:
        ValueError: Если e-mail уже зарегистрирован.
        RuntimeError: Если произошла ошибка базы данных или иная ошибка.
    """
    try:
        # Проверка существования пользователя с указанным e-mail
        existing_user = users_collection.find_one({"email": user.email})
        if existing_user:
            raise ValueError("Email already registered")

        # Хэширование пароля и сохранение данных пользователя
        hashed_password = hash_password(user.password)
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "hashed_password": hashed_password,
        }
        users_collection.insert_one(user_data)
        return {"msg": "User registered successfully"}
    except ValueError as ve:
        print(f"Validation error during registration: {ve}")
        raise ve
    except PyMongoError as pe:
        print(f"Database error during registration: {pe}")
        raise RuntimeError(
            "Database error occurred while registering a user"
        ) from pe
    except Exception as e:
        print(f"Unexpected error during registration: {e}")
        raise RuntimeError(
            "Unexpected error occurred during registration"
        ) from e


async def login_user_crud(user: UserLogin) -> Dict[str, str]:
    """
    Аутентификация пользователя.

    Если авторизация успешна, возвращается JWT-токен.

    Args:
        user (UserLogin): Данные для входа пользователя.

    Returns:
        Dict[str, str]: JWT-токен и его тип.

    Raises:
        ValueError: При неверных учетных данных.
        RuntimeError: При ошибке взаимодействия с базой данных.
    """
    try:
        # Поиск пользователя в базе данных по e-mail
        db_user = users_collection.find_one({"email": user.email})
        if not db_user or not verify_password(
                user.password, db_user["hashed_password"]
        ):
            raise ValueError("Invalid credentials")

        # Генерация JWT-токена
        token = create_access_token({"sub": user.email})
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as ve:
        print(f"Validation error during login: {ve}")
        raise ve
    except PyMongoError as pe:
        print(f"Database error during login: {pe}")
        raise RuntimeError(
            "Database error occurred while logging in"
        ) from pe
    except Exception as e:
        print(f"Unexpected error during login: {e}")
        raise RuntimeError(
            "Unexpected error occurred during login"
        ) from e
