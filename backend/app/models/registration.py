from datetime import datetime
from pydantic import BaseModel, Field, field_validator
import re


class Registration(BaseModel):
    """
    Модель регистрации транспортного средства.

    Атрибуты:
        license_plate (str): Номерной знак автомобиля.
            Формат - заглавные буквы, цифры и/или дефисы. Максимум 10 символов.
        owner_name (str): Имя владельца автомобиля.
            От 1 до 50 символов. Допускаются буквы, пробелы и дефисы.
        owner_address (str): Адрес владельца автомобиля.
            От 1 до 100 символов. Допускаются буквы, цифры, пробелы, точки, запятые и другие стандартные символы адреса.
        year_of_manufacture (int): Год выпуска автомобиля.
            Должен быть не меньше 1900 года и не превышать текущий год.
    """

    license_plate: str = Field(
        ...,
        pattern=r"^[A-Z0-9-]{1,10}$",
        description="Номерной знак автомобиля (до 10 символов)",
    )
    owner_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Имя владельца авто (от 1 до 50 символов)",
    )
    owner_address: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Адрес владельца (от 1 до 100 символов)",
    )
    year_of_manufacture: int = Field(
        ...,
        ge=1900,
        le=datetime.now().year,
        description="Год выпуска автомобиля (от 1900 до текущего года)",
    )

    @field_validator("owner_name")
    def validate_owner_name(cls, value: str) -> str:
        """
        Валидация имени владельца.

        Args:
            value (str): Имя для проверки.

        Returns:
            str: Прошедшее валидацию имя.

        Raises:
            ValueError: Если имя содержит недопустимые символы.
        """
        if not re.match(r"^[a-zA-Zа-яА-ЯёЁ\s\-]+$", value):
            raise ValueError(
                "Имя может содержать только буквы, пробелы и дефисы."
            )
        return value

    @field_validator("owner_address")
    def validate_owner_address(cls, value: str) -> str:
        """
        Валидация адреса владельца.

        Args:
            value (str): Адрес для проверки.

        Returns:
            str: Прошедший валидацию адрес.

        Raises:
            ValueError: Если адрес содержит недопустимые символы.
        """
        if not re.match(r"^[А-Яа-яЁёA-Za-z0-9\s.,\-\\/]+$", value):
            raise ValueError(
                "Адрес может содержать только буквы, цифры и символы: ., - \/"
            )
        return value

    @field_validator("license_plate")
    def validate_license_plate(cls, value: str) -> str:
        """
        Валидация номерного знака автомобиля.

        Args:
            value (str): Номерной знак для проверки.

        Returns:
            str: Прошедший валидацию номерной знак.

        Raises:
            ValueError: Если номерной знак содержит недопустимые символы.
        """
        pattern = r"^[A-Z0-9-]{1,10}$"
        if not re.match(pattern, value):
            raise ValueError(
                "Номерной знак должен содержать только заглавные буквы, цифры и/или дефисы (до 10 символов)."
            )
        return value
