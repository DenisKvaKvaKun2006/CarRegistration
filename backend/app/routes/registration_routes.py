from fastapi import APIRouter
from models.registration import Registration
from crud.registration_crud import add_registration, get_all_registrations, delete_registration_by_license_plate

router = APIRouter()


@router.post("/add_registration/")
async def add_registration_view(registration: Registration):
    add_registration(registration)
    return {"message": "Registration added successfully"}


@router.get("/get_registrations/")
async def get_registrations():
    registrations = get_all_registrations()
    return {"registrations": registrations}


@router.delete("/delete_registration/{license_plate}")
async def delete_registration(license_plate: str):
    delete_registration_by_license_plate(license_plate)
    return {"message": "Registration deleted successfully"}