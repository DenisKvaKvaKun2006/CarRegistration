from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """
    Модель для создания нового пользователя.

    Атрибуты:
        first_name (str): Имя пользователя. От 2 до 50 символов.
        last_name (str): Фамилия пользователя. От 2 до 50 символов.
        email (EmailStr): E-mail пользователя.
        password (str): Пароль пользователя. Минимум 6 символов.
        confirm_password (str): Подтверждение пароля. Минимум 6 символов.
    """
    first_name: str = Field(..., min_length=2, max_length=50, description="Имя пользователя (2-50 символов)")
    last_name: str = Field(..., min_length=2, max_length=50, description="Фамилия пользователя (2-50 символов)")
    email: EmailStr = Field(..., description="E-mail пользователя")
    password: str = Field(..., min_length=6, description="Пароль пользователя, минимум 6 символов")
    confirm_password: str = Field(..., min_length=6, description="Подтверждение пароля, минимум 6 символов")

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    """
    Модель для входа пользователя.

    Атрибуты:
        email (EmailStr): E-mail пользователя.
        password (str): Пароль пользователя.
    """
    email: EmailStr = Field(..., description="E-mail пользователя")
    password: str = Field(..., description="Пароль пользователя")
