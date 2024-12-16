from pydantic import BaseModel, Field, field_validator
import re


class Car(BaseModel):
    make: str = Field(..., min_length=1, max_length=50, description="Марка автомобиля")
    model: str = Field(..., min_length=1, max_length=50, description="Модель автомобиля")
    license_plate: str = Field(..., description="Номерной знак автомобиля")

    @field_validator("make")
    def validate_make(cls, value):
        if not re.match(r"^[A-Za-z\s-]{1,50}$", value):
            raise ValueError("Неверный формат марки автомобиля.")
        return value

    @field_validator("model")
    def validate_model(cls, value):
        if not re.match(r"^[A-Za-z0-9\s-]{1,50}$", value):
            raise ValueError("Неверный формат модели автомобиля.")
        return value

    @field_validator("license_plate")
    def validate_license_plate(cls, value):
        if not re.match(r"^[A-Z]{1}\d{3}[A-Z]{2}\d{2,3}$", value):
            raise ValueError(
                "Неверный формат номерного знака."
            )
        return value
