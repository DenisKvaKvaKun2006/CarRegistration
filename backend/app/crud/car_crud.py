from database import car_collection
from models.car import Car
from typing import List


def update_car_by_license_plate(license_plate: str, update_data: dict):
    """
    Редактировать данные автомобиля по его номеру.
    """
    try:
        update_data.pop("license_plate", None)
        result = car_collection.update_one(
            {"license_plate": license_plate},
            {"$set": update_data}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Error updating car: {e}")
        raise


def search_cars(query: str) -> List[Car]:
    """
    Поиск автомобилей по строке в любом из полей.
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

    except Exception as e:
        print(f"Error searching cars: {e}")
        raise


def add_car(car: Car):
    try:
        car_collection.insert_one(car.dict())
    except Exception as e:
        print(f"Error adding car: {e}")
        raise


def delete_car_by_license_plate(license_plate: str):
    try:
        result = car_collection.delete_one({"license_plate": license_plate})
        if result.deleted_count == 0:
            print("No car found with the given license plate.")
        return result
    except Exception as e:
        print(f"Error deleting car: {e}")
        raise


def get_all_cars() -> List[Car]:
    try:
        cars = car_collection.find()
        return [Car(**{**car, "id": str(car["_id"])}) for car in cars]
    except Exception as e:
        print(f"Error fetching cars: {e}")
        raise
