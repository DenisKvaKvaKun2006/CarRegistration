from pydantic import BaseModel


class Registration(BaseModel):
    license_plate: str
    owner_name: str
    owner_address: str
    year_of_manufacture: int
