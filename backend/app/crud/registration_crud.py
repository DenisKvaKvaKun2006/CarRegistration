from database import registration_collection
from models.registration import Registration
from typing import List


def update_registration_by_license_plate(license_plate: str, update_data: dict):
    """
    Редактировать данные регистрации по её номеру.
    """
    try:
        update_data.pop("license_plate", None)
        result = registration_collection.update_one(
            {"license_plate": license_plate},
            {"$set": update_data}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Error updating registration: {e}")
        raise


def search_registrations(query: str) -> List[Registration]:
    """
    Поиск регистраций по строке в любом из полей.
    """
    try:
        registrations = registration_collection.find({
            "$or": [
                {"license_plate": {"$regex": query, "$options": "i"}},
                {"owner_name": {"$regex": query, "$options": "i"}},
                {"owner_address": {"$regex": query, "$options": "i"}}
            ]
        })
        registrations_list = [Registration(**{**registration, "id": str(registration["_id"])}) for registration in
                              registrations]
        return registrations_list

    except Exception as e:
        print(f"Error searching registrations: {e}")
        raise


def add_registration(registration: Registration):
    try:
        registration_collection.insert_one(registration.dict())
    except Exception as e:
        print(f"Error adding registration: {e}")
        raise


def get_all_registrations() -> List[Registration]:
    try:
        registrations = registration_collection.find()
        return [Registration(**{**registration, "id": str(registration["_id"])}) for registration in registrations]
    except Exception as e:
        print(f"Error fetching registrations: {e}")
        raise


def delete_registration_by_license_plate(license_plate: str):
    try:
        result = registration_collection.delete_one({"license_plate": license_plate})
        if result.deleted_count == 0:
            print("No registration found with the given license plate.")
        return result
    except Exception as e:
        print(f"Error deleting registration: {e}")
        raise
