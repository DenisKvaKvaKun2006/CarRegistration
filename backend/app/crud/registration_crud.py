from database import registration_collection
from models.registration import Registration
from typing import List


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
    except Exception as e:
        print(f"Error deleting registration: {e}")
        raise