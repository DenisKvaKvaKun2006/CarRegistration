from fastapi import APIRouter, Depends, HTTPException
from models.car import Car
from crud.car_crud import (
    add_car,
    delete_car_by_license_plate,
    get_all_cars,
    search_cars,
    update_car_by_license_plate
)
from security.jwt import decode_access_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# Функция для получения текущего пользователя
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload.get("sub")


router = APIRouter()


@router.put(
    "/update_car/{license_plate}",
    responses={
        200: {"description": "Car was successfully updated"},
        400: {"description": "Validation error (e.g., license plate modification not allowed)"},
        404: {"description": "Car not found or no updates applied"},
        500: {"description": "Unexpected error during car update"},
    },
)
async def update_car_view(license_plate: str, update_data: dict, user: str = Depends(get_current_user)):
    """
    Редактировать данные автомобиля. Номер автомобиля редактировать запрещено.
    """
    try:
        updated = update_car_by_license_plate(license_plate, update_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Car not found or no updates applied")
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
async def search_cars_view(query: str, user: str = Depends(get_current_user)):
    """
    Поиск автомобилей по марке, модели или номерному знаку.
    """
    try:
        cars = search_cars(query)
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
async def add_car_view(car: Car, user: str = Depends(get_current_user)):
    """
    Добавление автомобиля.
    """
    try:
        add_car(car)
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
async def delete_car_view(license_plate: str, user: str = Depends(get_current_user)):
    """
    Удаление автомобиля.
    """
    try:
        delete_car_by_license_plate(license_plate)
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
async def get_cars(user: str = Depends(get_current_user)):
    """
    Получение всех автомобилей.
    """
    try:
        cars = get_all_cars()
        return {"cars": cars, "user": user}
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
