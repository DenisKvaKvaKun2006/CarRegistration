from typing import List, Dict
from pymongo.errors import PyMongoError
from database import car_collection
from models.car import Car


async def update_car_by_license_plate(license_plate: str, update_data: Dict) -> bool:
    """
    Обновление автомобиля по номерному знаку (license_plate).

    Запрещено изменять ключ 'license_plate' в update_data.

    Args:
        license_plate (str): Номерной знак автомобиля.
        update_data (Dict): Данные для обновления автомобиля.

    Returns:
        bool: True, если обновление завершено успешно, иначе False.

    Raises:
        ValueError: Если 'license_plate' в update_data или автомобиль отсутствует.
        RuntimeError: При ошибке взаимодействия с базой данных.
    """
    try:
        if "license_plate" in update_data:
            raise ValueError("Updating license plate is not allowed")

        result = car_collection.update_one(
            {"license_plate": license_plate},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise ValueError("Car not found")
        return result.modified_count > 0
    except ValueError as ve:
        print(f"Validation error during update: {ve}")
        raise ve
    except PyMongoError as pe:
        print(f"Database error during update: {pe}")
        raise RuntimeError("Database error occurred while updating the car") from pe
    except Exception as e:
        print(f"Unexpected error during update: {e}")
        raise RuntimeError("Unexpected error occurred while updating the car") from e


async def search_cars(query: str) -> List[Car]:
    """
    Поиск автомобилей по запросу.

    Args:
        query (str): Запрос для поиска (марка, модель или номерной знак).

    Returns:
        List[Car]: Список объектов Car, соответствующих запросу.

    Raises:
        RuntimeError: При ошибке взаимодействия с базой данных.
    """
    try:
        cars = car_collection.find({
            "$or": [
                {"make": {"$regex": query, "$options": "i"}},
                {"model": {"$regex": query, "$options": "i"}},
                {"license_plate": {"$regex": query, "$options": "i"}}
            ]
        })
        return [Car(**{**car, "id": str(car["_id"])}) for car in cars]
    except PyMongoError as pe:
        print(f"Database error during search: {pe}")
        raise RuntimeError("Database error occurred while searching cars") from pe
    except Exception as e:
        print(f"Unexpected error during search: {e}")
        raise RuntimeError("Unexpected error occurred while searching cars") from e


async def add_car(car: Car) -> None:
    """
    Добавление нового автомобиля.

    Номерной знак (license_plate) должен быть уникальным.

    Args:
        car (Car): Объект нового автомобиля.

    Raises:
        ValueError: Если автомобиль с таким номерным знаком уже существует.
        RuntimeError: При ошибке взаимодействия с базой данных.
    """
    try:
        if car_collection.find_one({"license_plate": car.license_plate}):
            raise ValueError("Car with given license plate already exists")

        car_collection.insert_one(car.dict())
    except ValueError as ve:
        print(f"Validation error during addition: {ve}")
        raise ve
    except PyMongoError as pe:
        print(f"Database error during addition: {pe}")
        raise RuntimeError("Database error occurred while adding a car") from pe
    except Exception as e:
        print(f"Unexpected error during addition: {e}")
        raise RuntimeError("Unexpected error occurred while adding a car") from e


async def delete_car_by_license_plate(license_plate: str) -> bool:
    """
    Удаление автомобиля по номерному знаку (license_plate).

    Args:
        license_plate (str): Номерной знак автомобиля для удаления.

    Returns:
        bool: True, если удаление прошло успешно, иначе False.

    Raises:
        ValueError: Если автомобиль с указанным номерным знаком отсутствует.
        RuntimeError: При ошибке взаимодействия с базой данных.
    """
    try:
        result = car_collection.delete_one({"license_plate": license_plate})
        if result.deleted_count == 0:
            raise ValueError("Car with given license plate not found")
        return result.deleted_count > 0
    except ValueError as ve:
        print(f"Validation error during deletion: {ve}")
        raise ve
    except PyMongoError as pe:
        print(f"Database error during deletion: {pe}")
        raise RuntimeError("Database error occurred while deleting the car") from pe
    except Exception as e:
        print(f"Unexpected error during deletion: {e}")
        raise RuntimeError("Unexpected error occurred while deleting the car") from e


async def get_all_cars() -> List[Car]:
    """
    Получение списка всех автомобилей.

    Returns:
        List[Car]: Список всех объектов Car.

    Raises:
        RuntimeError: При ошибке взаимодействия с базой данных.
    """
    try:
        cars = car_collection.find()
        return [Car(**{**car, "id": str(car["_id"])}) for car in cars]
    except PyMongoError as pe:
        print(f"Database error during fetching all cars: {pe}")
        raise RuntimeError("Database error occurred while fetching all cars") from pe
    except Exception as e:
        print(f"Unexpected error during fetching all cars: {e}")
        raise RuntimeError("Unexpected error occurred while fetching all cars") from e
