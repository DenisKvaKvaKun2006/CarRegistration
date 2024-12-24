from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from models.registration import Registration
from crud.registration_crud import (
    add_registration,
    get_all_registrations,
    delete_registration_by_license_plate,
    search_registrations,
    update_registration_by_license_plate,
)
from security.jwt import decode_access_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Получение текущего пользователя на основе переданного токена.

    Args:
        token (str): OAuth2 токен пользователя.

    Returns:
        str: Идентификатор пользователя.

    Raises:
        HTTPException: Если токен недействителен или истек.
    """
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload.get("sub")


@router.put(
    "/update_registration/{license_plate}",
    responses={
        200: {"description": "Registration was successfully updated"},
        400: {"description": "Validation error (e.g., license plate modification not allowed)"},
        404: {"description": "Registration not found or no updates applied"},
        500: {"description": "Unexpected error during registration update"},
    },
)
async def update_registration_view(
        license_plate: str,
        update_data: Dict[str, Any],
        user: str = Depends(get_current_user),
) -> Dict[str, str]:
    """
    Обновление данных регистрации.

    Args:
        license_plate (str): Номерной знак, идентифицирующий регистрацию.
        update_data (Dict[str, Any]): Данные для обновления регистрации.
        user (str): Текущий пользователь, извлеченный из токена (определяется через Depends).

    Returns:
        Dict[str, str]: Сообщение о статусе обновления.

    Raises:
        HTTPException: Если регистрация не найдена, есть ошибки валидации или произошла ошибка на сервере.
    """
    try:
        updated = await update_registration_by_license_plate(license_plate, update_data)
        if not updated:
            raise HTTPException(
                status_code=404, detail="Registration not found or no updates applied"
            )
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
async def search_registrations_view(
        query: str, user: str = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Поиск регистраций.

    Args:
        query (str): Запрос для поиска регистраций.
        user (str): Текущий пользователь, извлеченный из токена (определяется через Depends).

    Returns:
        Dict[str, Any]: Найденные регистрации и сообщение о статусе поиска.

    Raises:
        HTTPException: Если произошла ошибка на сервере.
    """
    try:
        registrations = await search_registrations(query)
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
async def add_registration_view(
        registration: Registration, user: str = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Добавление новой регистрации.

    Args:
        registration (Registration): Данные регистрации.
        user (str): Текущий пользователь, извлеченный из токена (определяется через Depends).

    Returns:
        Dict[str, str]: Сообщение о статусе добавления.

    Raises:
        HTTPException: Если есть ошибка валидации или произошла ошибка на сервере.
    """
    try:
        await add_registration(registration)
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
async def get_registrations(user: str = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Получение всех регистраций.

    Args:
        user (str): Текущий пользователь, извлеченный из токена (определяется через Depends).

    Returns:
        Dict[str, Any]: Список всех регистраций.

    Raises:
        HTTPException: Если произошла ошибка на сервере.
    """
    try:
        registrations = await get_all_registrations()
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
async def delete_registration_view(
        license_plate: str, user: str = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Удаление регистрации.

    Args:
        license_plate (str): Номерной знак, идентифицирующий регистрацию.
        user (str): Текущий пользователь, извлеченный из токена (определяется через Depends).

    Returns:
        Dict[str, str]: Сообщение о статусе удаления.

    Raises:
        HTTPException: Если регистрация не найдена или произошла ошибка на сервере.
    """
    try:
        await delete_registration_by_license_plate(license_plate)
        return {"message": f"Registration deleted successfully by {user}"}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
