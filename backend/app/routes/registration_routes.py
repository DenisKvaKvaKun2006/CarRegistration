from fastapi import APIRouter, Depends, HTTPException
from models.registration import Registration
from crud.registration_crud import (
    add_registration,
    get_all_registrations,
    delete_registration_by_license_plate,
    search_registrations,
    update_registration_by_license_plate
)
from security.jwt import decode_access_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload.get("sub")


router = APIRouter()


@router.put(
    "/update_registration/{license_plate}",
    responses={
        200: {"description": "Registration was successfully updated"},
        400: {"description": "Validation error (e.g., license plate modification not allowed)"},
        404: {"description": "Registration not found or no updates applied"},
        500: {"description": "Unexpected error during registration update"},
    },
)
async def update_registration_view(license_plate: str, update_data: dict, user: str = Depends(get_current_user)):
    """
    Обновление данных регистрации.
    """
    try:
        updated = update_registration_by_license_plate(license_plate, update_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Registration not found or no updates applied")
        return {"message": f"Registration updated successfully by {user}"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))


@router.get(
    "/search_registrations/",
    responses={
        200: {"description": "Registrations searched successfully. Results returned."},
        500: {"description": "Unexpected error during registrations search"},
    },
)
async def search_registrations_view(query: str, user: str = Depends(get_current_user)):
    """
    Поиск регистраций.
    """
    try:
        registrations = search_registrations(query)
        if not registrations:
            return {"registrations": [], "message": "No registrations found matching the query."}
        return {"registrations": registrations}
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))


@router.post(
    "/add_registration/",
    responses={
        200: {"description": "Registration successfully added"},
        400: {"description": "Validation error (e.g., duplicate license plate)"},
        500: {"description": "Unexpected error during registration addition"},
    },
)
async def add_registration_view(registration: Registration, user: str = Depends(get_current_user)):
    """
    Добавление новой регистрации.
    """
    try:
        add_registration(registration)
        return {"message": f"Registration added successfully by {user}"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))


@router.get(
    "/get_registrations/",
    responses={
        200: {"description": "All registrations successfully retrieved"},
        500: {"description": "Unexpected error during registrations retrieval"},
    },
)
async def get_registrations(user: str = Depends(get_current_user)):
    """
    Получение всех регистраций.
    """
    try:
        registrations = get_all_registrations()
        return {"registrations": registrations, "user": user}
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))


@router.delete(
    "/delete_registration/{license_plate}",
    responses={
        200: {"description": "Registration successfully deleted"},
        404: {"description": "Registration not found"},
        500: {"description": "Unexpected error during registration deletion"},
    },
)
async def delete_registration_view(license_plate: str, user: str = Depends(get_current_user)):
    """
    Удаление регистрации.
    """
    try:
        delete_registration_by_license_plate(license_plate)
        return {"message": f"Registration deleted successfully by {user}"}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
