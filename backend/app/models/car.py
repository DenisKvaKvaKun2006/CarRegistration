from pydantic import BaseModel


class Car(BaseModel):
    make: str
    model: str
    license_plate: str
