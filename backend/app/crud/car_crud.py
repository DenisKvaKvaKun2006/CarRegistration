from database import car_collection
from models.car import Car
from typing import List
from pymongo.errors import PyMongoError


def update_car_by_license_plate(license_plate: str, update_data: dict):
    """
    Обновление автомобиля по номеру.
    """
    try:
        # Проверяем, чтобы нельзя было изменить license_plate
        if "license_plate" in update_data:
            raise ValueError("Updating license plate is not allowed")

        # Выполняем обновление
        result = car_collection.update_one(
            {"license_plate": license_plate},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise ValueError("Car not found")
        return result.modified_count > 0
    except ValueError as ve:
        # Валидация данных или отсутствие сущности
        print(f"Validation error during update: {ve}")
        raise ve
    except PyMongoError as pe:
        # Ошибка базы данных
        print(f"Database error: {pe}")
        raise RuntimeError("Database error occurred while updating the car")
    except Exception as e:
        print(f"Unexpected error during update: {e}")
        raise RuntimeError("Unexpected error occurred while updating the car")


def search_cars(query: str) -> List[Car]:
    """
    Поиск автомобилей.
    """
    try:
        cars = car_collection.find({
            "$or": [
                {"make": {"$regex": query, "$options": "i"}},
                {"model": {"$regex": query, "$options": "i"}},
                {"license_plate": {"$regex": query, "$options": "i"}}
            ]
        })
        cars_list = [Car(**{**car, "id": str(car["_id"])}) for car in cars]
        return cars_list
    except PyMongoError as pe:
        print(f"Database error during search: {pe}")
        raise RuntimeError("Database error occurred while searching cars")
    except Exception as e:
        print(f"Unexpected error during search: {e}")
        raise RuntimeError("Unexpected error occurred while searching cars")


def add_car(car: Car):
    """
    Добавление нового автомобиля.
    """
    try:
        # Проверка на дублирование license_plate
        if car_collection.find_one({"license_plate": car.license_plate}):
            raise ValueError("Car with given license plate already exists")

        car_collection.insert_one(car.dict())
    except ValueError as ve:
        print(f"Validation error during addition: {ve}")
        raise ve
    except PyMongoError as pe:
        print(f"Database error during addition: {pe}")
        raise RuntimeError("Database error occurred while adding a car")
    except Exception as e:
        print(f"Unexpected error during addition: {e}")
        raise RuntimeError("Unexpected error occurred while adding a car")


def delete_car_by_license_plate(license_plate: str):
    """
    Удаление автомобиля по номеру.
    """
    try:
        result = car_collection.delete_one({"license_plate": license_plate})
        if result.deleted_count == 0:
            raise ValueError("Car with given license plate not found")
        return result
    except ValueError as ve:
        print(f"Validation error during deletion: {ve}")
        raise ve
    except PyMongoError as pe:
        print(f"Database error during deletion: {pe}")
        raise RuntimeError("Database error occurred while deleting the car")
    except Exception as e:
        print(f"Unexpected error during deletion: {e}")
        raise RuntimeError("Unexpected error occurred while deleting the car")


def get_all_cars() -> List[Car]:
    """
    Получение всех автомобилей.
    """
    try:
        cars = car_collection.find()
        return [Car(**{**car, "id": str(car["_id"])}) for car in cars]
    except PyMongoError as pe:
        print(f"Database error during fetching all cars: {pe}")
        raise RuntimeError("Database error occurred while fetching all cars")
    except Exception as e:
        print(f"Unexpected error during fetching all cars: {e}")
        raise RuntimeError("Unexpected error occurred while fetching all cars")