from fastapi import APIRouter
from models.car import Car
from crud.car_crud import add_car, delete_car_by_license_plate, get_all_cars
router = APIRouter()

# Добавление машины
@router.post("/add_car/")
async def add_car_view(car: Car):
    add_car(car)
    return {"message": "Car added successfully"}

# Удаление машины по номеру
@router.delete("/delete_car/{license_plate}")
async def delete_car_view(license_plate: str):
    delete_car_by_license_plate(license_plate)
    return {"message": "Car deleted successfully"}

# Получение всех машин
@router.get("/get_cars/")
async def get_cars():
    cars = get_all_cars()
    return {"cars": cars}