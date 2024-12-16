from pydantic import BaseModel, Field, field_validator
import re


class Car(BaseModel):
    """
    Модель для представления автомобиля.

    Attributes:
        make (str): Марка автомобиля.
        model (str): Модель автомобиля.
        license_plate (str): Номерной знак автомобиля.
    """
    make: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Марка автомобиля (1–50 символов)"
    )
    model: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Модель автомобиля (1–50 символов)"
    )
    license_plate: str = Field(
        ...,
        description="Номерной знак автомобиля (строковый формат)"
    )

    @field_validator("make")
    def validate_make(cls, value: str) -> str:
        """
        Проверяет, что марка автомобиля содержит только допустимые символы.

        Args:
            value (str): Значение поля make.

        Returns:
            str: Валидное значение поля make.

        Raises:
            ValueError: Если значение содержит недопустимые символы.
        """
        if not re.match(r"^[A-Za-z\s-]{1,50}$", value):
            raise ValueError("Марка автомобиля содержит недопустимые символы.")
        return value

    @field_validator("model")
    def validate_model(cls, value: str) -> str:
        """
        Проверяет, что модель автомобиля содержит только допустимые символы.

        Args:
            value (str): Значение поля model.

        Returns:
            str: Валидное значение поля model.

        Raises:
            ValueError: Если значение содержит недопустимые символы.
        """
        if not re.match(r"^[A-Za-z0-9\s-]{1,50}$", value):
            raise ValueError("Модель автомобиля содержит недопустимые символы.")
        return value

    @field_validator("license_plate")
    def validate_license_plate(cls, value: str) -> str:
        """
        Проверяет, что номерной знак автомобиля имеет валидный формат.

        Args:
            value (str): Значение поля license_plate.

        Returns:
            str: Валидное значение поля license_plate.

        Raises:
            ValueError: Если значение не соответствует формату номерного знака.
        """
        if not re.match(r"^[A-Z0-9]{3,10}$", value):
            raise ValueError("Номерной знак имеет некорректный формат.")
        return value
