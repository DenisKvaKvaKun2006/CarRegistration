from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re


class Registration(BaseModel):
    license_plate: str = Field(..., pattern=r"^[A-Z0-9-]{1,10}$", description="Номерной знак автомобиля")
    owner_name: str = Field(..., min_length=1, max_length=50, description="Имя владельца авто")
    owner_address: str = Field(..., min_length=1, max_length=100, description="Адрес владельца")
    year_of_manufacture: int = Field(..., ge=1900, le=datetime.now().year, description="Год выпуска")

    @field_validator("owner_name")
    def validate_owner_name(cls, value):
        if not re.match(r"^[a-zA-Zа-яА-ЯёЁ\s\-]+$", value):
            raise ValueError("Неверный формат имени.")
        return value

    @field_validator("owner_address")
    def validate_owner_address(cls, value):
        if not re.match(r"^[А-Яа-яЁёA-Za-z0-9\s.,-\\/]+$", value):
            raise ValueError("Неверный формат адреса.")
        return value

    @field_validator("license_plate")
    def validate_license_plate(cls, value):
        if not re.match(r"^[A-Z]{1}\d{3}[A-Z]{2}\d{2,3}$", value):
            raise ValueError(
                "Неверный формат номерного знака."
            )
        return value
