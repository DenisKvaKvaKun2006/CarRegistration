from database import car_collection
from models.car import Car
from typing import List


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
