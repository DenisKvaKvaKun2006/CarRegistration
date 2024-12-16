from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Хэширование пароля.

    Args:
        password (str): Пароль в виде обычной строки для хэширования.

    Returns:
        str: Хэшированный пароль.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Сравнение введенного пароля с хэшированным.

    Args:
        plain_password (str): Введенный пароль в виде обычной строки.
        hashed_password (str): Хэшированный пароль.

    Returns:
        bool: True, если пароли совпадают, иначе False.
    """
    return pwd_context.verify(plain_password, hashed_password)
