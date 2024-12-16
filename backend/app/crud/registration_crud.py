from database import registration_collection
from models.registration import Registration
from typing import List
from pymongo.errors import PyMongoError


def update_registration_by_license_plate(license_plate: str, update_data: dict):
    """
    Редактировать данные регистрации по её номеру.
    """
    try:
        # Запрещаем изменение license_plate
        if "license_plate" in update_data:
            raise ValueError("Updating license plate is not allowed")

        # Выполняем обновление
        result = registration_collection.update_one(
            {"license_plate": license_plate},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise ValueError("Registration not found")
        return result.modified_count > 0
    except ValueError as ve:
        print(f"Validation Error during update: {ve}")
        raise ve
    except PyMongoError as pe:
        print(f"Database Error during update: {pe}")
        raise RuntimeError("Database error occurred during update")
    except Exception as e:
        print(f"Unexpected Error during update: {e}")
        raise RuntimeError("Unexpected error occurred during update")


def search_registrations(query: str) -> List[Registration]:
    """
    Поиск регистраций в базе.
    """
    try:
        registrations = registration_collection.find({
            "$or": [
                {"license_plate": {"$regex": query, "$options": "i"}},
                {"owner_name": {"$regex": query, "$options": "i"}},
                {"owner_address": {"$regex": query, "$options": "i"}}
            ]
        })
        registrations_list = [
            Registration(**{**registration, "id": str(registration["_id"])})
            for registration in registrations
        ]
        return registrations_list
    except PyMongoError as pe:
        print(f"Database error during search: {pe}")
        raise RuntimeError("Database error occurred while searching registrations")
    except Exception as e:
        print(f"Unexpected error during search: {e}")
        raise RuntimeError("Unexpected error occurred while searching registrations")


def add_registration(registration: Registration):
    """
    Добавление новой регистрации.
    """
    try:
        # Проверяем на дублирующий license_plate
        if registration_collection.find_one({"license_plate": registration.license_plate}):
            raise ValueError("Registration with given license plate already exists")

        registration_collection.insert_one(registration.dict())
    except ValueError as ve:
        print(f"Validation Error during addition: {ve}")
        raise ve
    except PyMongoError as pe:
        print(f"Database error during addition: {pe}")
        raise RuntimeError("Database error occurred while adding registration")
    except Exception as e:
        print(f"Unexpected error during addition: {e}")
        raise RuntimeError("Unexpected error occurred while adding registration")


def get_all_registrations() -> List[Registration]:
    """
    Получение всех регистраций.
    """
    try:
        registrations = registration_collection.find()
        return [
            Registration(**{**registration, "id": str(registration["_id"])})
            for registration in registrations
        ]
    except PyMongoError as pe:
        print(f"Database error during fetching registrations: {pe}")
        raise RuntimeError("Database error occurred while fetching registrations")
    except Exception as e:
        print(f"Unexpected error during fetching registrations: {e}")
        raise RuntimeError("Unexpected error occurred while fetching registrations")


def delete_registration_by_license_plate(license_plate: str):
    """
    Удаление регистрации по номеру.
    """
    try:
        result = registration_collection.delete_one({"license_plate": license_plate})
        if result.deleted_count == 0:
            raise ValueError("Registration not found")
        return result
    except ValueError as ve:
        print(f"Validation Error during deletion: {ve}")
        raise ve
    except PyMongoError as pe:
        print(f"Database error during deletion: {pe}")
        raise RuntimeError("Database error occurred while deleting registration")
    except Exception as e:
        print(f"Unexpected error during deletion: {e}")
        raise RuntimeError("Unexpected error occurred while deleting registration")
