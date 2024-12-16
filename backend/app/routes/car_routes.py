from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models.car import Car
from crud.car_crud import (
    add_car,
    delete_car_by_license_plate,
    get_all_cars,
    search_cars,
    update_car_by_license_plate,
)
from security.jwt import decode_access_token
from typing import Dict, Any

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


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


router = APIRouter()


@router.put(
    "/update_car/{license_plate}",
    responses={
        200: {"description": "Car was successfully updated"},
        400: {
            "description": "Validation error (e.g., license plate modification not allowed)"
        },
        404: {"description": "Car not found or no updates applied"},
        500: {"description": "Unexpected error during car update"},
    },
)
async def update_car_view(
        license_plate: str, update_data: Dict[str, Any], user: str = Depends(get_current_user)
) -> Dict[str, str]:
    """
    Редактирование данных автомобиля. Номер автомобиля редактировать запрещено.

    Args:
        license_plate (str): Номерной знак автомобиля.
        update_data (Dict[str, Any]): Данные для обновления.
        user (str): ID текущего пользователя (из токена).

    Returns:
        Dict[str, str]: Сообщение об успешном обновлении автомобиля.

    Raises:
        HTTPException: При возникновении ошибки.
    """
    try:
        updated = await update_car_by_license_plate(license_plate, update_data)
        if not updated:
            raise HTTPException(
                status_code=404, detail="Car not found or no updates applied"
            )
        return {"message": f"Car updated successfully by {user}"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))


@router.get(
    "/search_cars/",
    responses={
        200: {"description": "Cars searched successfully. Results returned."},
        500: {"description": "Unexpected error occurred while searching cars"},
    },
)
async def search_cars_view(query: str, user: str = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Поиск автомобилей по марке, модели или номерному знаку.

    Args:
        query (str): Запрос для поиска.
        user (str): ID текущего пользователя (из токена).

    Returns:
        Dict[str, Any]: Найденные автомобили и данные текущего пользователя.

    Raises:
        HTTPException: При возникновении ошибки.
    """
    try:
        cars = await search_cars(query)
        if not cars:
            return {"cars": [], "message": "No cars found matching the query."}
        return {"cars": cars, "user": user}
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))


@router.post(
    "/add_car/",
    responses={
        200: {"description": "Car successfully added"},
        400: {"description": "Validation error (e.g., duplicate license plate)"},
        500: {"description": "Unexpected error during car addition"},
    },
)
async def add_car_view(car: Car, user: str = Depends(get_current_user)) -> Dict[str, str]:
    """
    Добавление автомобиля.

    Args:
        car (Car): Данные добавляемого автомобиля.
        user (str): ID текущего пользователя (из токена).

    Returns:
        Dict[str, str]: Сообщение об успешном добавлении автомобиля.

    Raises:
        HTTPException: При возникновении ошибки.
    """
    try:
        await add_car(car)
        return {"message": f"Car added successfully by {user}"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))


@router.delete(
    "/delete_car/{license_plate}",
    responses={
        200: {"description": "Car successfully deleted"},
        404: {"description": "Car not found"},
        500: {"description": "Unexpected error during car deletion"},
    },
)
async def delete_car_view(license_plate: str, user: str = Depends(get_current_user)) -> Dict[str, str]:
    """
    Удаление автомобиля.

    Args:
        license_plate (str): Номерной знак удаляемого автомобиля.
        user (str): ID текущего пользователя (из токена).

    Returns:
        Dict[str, str]: Сообщение об успешном удалении автомобиля.

    Raises:
        HTTPException: При возникновении ошибки.
    """
    try:
        await delete_car_by_license_plate(license_plate)
        return {"message": f"Car deleted successfully by {user}"}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))


@router.get(
    "/get_cars/",
    responses={
        200: {"description": "All cars successfully retrieved"},
        500: {"description": "Unexpected error during cars retrieval"},
    },
)
async def get_cars(user: str = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Получение всех автомобилей.

    Args:
        user (str): ID текущего пользователя (из токена).

    Returns:
        Dict[str, Any]: Список всех автомобилей и данные пользователя.

    Raises:
        HTTPException: При возникновении ошибки.
    """
    try:
        cars = await get_all_cars()
        return {"cars": cars, "user": user}
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
