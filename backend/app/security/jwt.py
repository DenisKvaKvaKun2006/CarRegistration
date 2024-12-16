from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY: str = "keykeykey"  # Пусть будет так))
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


def create_access_token(data: dict) -> str:
    """
    Создание JWT-токена доступа.

    Args:
        data (dict): Данные, которые нужно закодировать в токен.

    Returns:
        str: Сформированный JWT-токен.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_access_token(token: str) -> Optional[dict]:
    """
    Расшифровка и валидация JWT-токена.

    Args:
        token (str): Токен доступа, который нужно расшифровать.

    Returns:
        Optional[dict]: Расшифрованные данные из токена, если токен валиден.
                        Возвращает None, если в процессе валидации токен оказался невалидным.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
