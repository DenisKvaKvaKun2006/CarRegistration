from database import registration_collection
from models.registration import Registration
from typing import List, Dict, Union
from pymongo.errors import PyMongoError


async def update_registration_by_license_plate(
        license_plate: str, update_data: Dict[str, Union[str, int]]
) -> bool:
    """
    Редактировать данные регистрации по её номеру.

    Args:
        license_plate (str): Номерной знак, соответствующий записи.
        update_data (Dict[str, Union[str, int]]): Данные для обновления
                                                  (кроме license_plate).

    Returns:
        bool: Статус успешности изменения.

    Raises:
        ValueError: Если попытка изменить license_plate или запись не найдена.
        RuntimeError: Если произошла ошибка базы данных или иная ошибка.
    """
    try:
        if "license_plate" in update_data:
            raise ValueError("Updating license plate is not allowed")

        result = registration_collection.update_one(
            {"license_plate": license_plate},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise ValueError("Registration not found")

        return result.modified_count > 0
    except ValueError as ve:
        print(f"Validation error during update: {ve}")
        raise ve
    except PyMongoError as pe:
        print(f"Database error during update: {pe}")
        raise RuntimeError("Database error occurred during update") from pe
    except Exception as e:
        print(f"Unexpected error during update: {e}")
        raise RuntimeError("Unexpected error occurred during update") from e


async def search_registrations(query: str) -> List[Registration]:
    """
    Поиск регистраций в базе данных по заданному запросу.

    Args:
        query (str): Поисковый запрос.

    Returns:
        List[Registration]: Список найденных регистраций.

    Raises:
        RuntimeError: Если произошла ошибка базы данных или иная ошибка.
    """
    try:
        registrations = registration_collection.find({
            "$or": [
                {"license_plate": {"$regex": query, "$options": "i"}},
                {"owner_name": {"$regex": query, "$options": "i"}},
                {"owner_address": {"$regex": query, "$options": "i"}}
            ]
        })
        return [
            Registration(**{**registration, "id": str(registration["_id"])})
            for registration in registrations
        ]
    except PyMongoError as pe:
        print(f"Database error during search: {pe}")
        raise RuntimeError(
            "Database error occurred while searching registrations"
        ) from pe
    except Exception as e:
        print(f"Unexpected error during search: {e}")
        raise RuntimeError(
            "Unexpected error occurred while searching registrations"
        ) from e


async def add_registration(registration: Registration) -> None:
    """
    Добавление новой регистрации.

    Args:
        registration (Registration): Объект регистрации.

    Raises:
        ValueError: Если регистрация с таким license_plate уже существует.
        RuntimeError: Если произошла ошибка базы данных или иная ошибка.
    """
    try:
        if registration_collection.find_one(
                {"license_plate": registration.license_plate}
        ):
            raise ValueError("Registration with given license plate already exists")

        registration_collection.insert_one(registration.dict())
    except ValueError as ve:
        print(f"Validation error during addition: {ve}")
        raise ve
    except PyMongoError as pe:
        print(f"Database error during addition: {pe}")
        raise RuntimeError(
            "Database error occurred while adding registration"
        ) from pe
    except Exception as e:
        print(f"Unexpected error during addition: {e}")
        raise RuntimeError(
            "Unexpected error occurred while adding registration"
        ) from e


async def get_all_registrations() -> List[Registration]:
    """
    Получение всех регистраций.

    Returns:
        List[Registration]: Список всех регистраций.

    Raises:
        RuntimeError: Если произошла ошибка базы данных или иная ошибка.
    """
    try:
        registrations = registration_collection.find()
        return [
            Registration(**{**registration, "id": str(registration["_id"])})
            for registration in registrations
        ]
    except PyMongoError as pe:
        print(f"Database error during fetching registrations: {pe}")
        raise RuntimeError(
            "Database error occurred while fetching registrations"
        ) from pe
    except Exception as e:
        print(f"Unexpected error during fetching registrations: {e}")
        raise RuntimeError(
            "Unexpected error occurred while fetching registrations"
        ) from e


async def delete_registration_by_license_plate(license_plate: str) -> bool:
    """
    Удаление регистрации по номеру.

    Args:
        license_plate (str): Номерной знак для удаления.

    Returns:
        bool: Статус успешности удаления.

    Raises:
        ValueError: Если запись с указанным номером не найдена.
        RuntimeError: Если произошла ошибка базы данных или иная ошибка.
    """
    try:
        result = registration_collection.delete_one({"license_plate": license_plate})
        if result.deleted_count == 0:
            raise ValueError("Registration not found")

        return result.deleted_count > 0
    except ValueError as ve:
        print(f"Validation error during deletion: {ve}")
        raise ve
    except PyMongoError as pe:
        print(f"Database error during deletion: {pe}")
        raise RuntimeError(
            "Database error occurred while deleting registration"
        ) from pe
    except Exception as e:
        print(f"Unexpected error during deletion: {e}")
        raise RuntimeError(
            "Unexpected error occurred while deleting registration"
        ) from e
