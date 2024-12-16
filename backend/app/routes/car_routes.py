from fastapi import APIRouter, Depends, HTTPException
from models.car import Car
from crud.car_crud import add_car, delete_car_by_license_plate, get_all_cars, search_cars, update_car_by_license_plate
from security.jwt import decode_access_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload.get("sub")


router = APIRouter()


@router.put("/update_car/{license_plate}")
async def update_car_view(license_plate: str, update_data: dict, user: str = Depends(get_current_user)):
    """
    Редактировать данные автомобиля. Номер автомобиля редактировать запрещено.
    """
    try:
        updated = update_car_by_license_plate(license_plate, update_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Car not found or no updates applied")
        return {"message": f"Car updated successfully by {user}"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update car: {str(e)}")


@router.get("/search_cars/")
async def search_cars_view(query: str, user: str = Depends(get_current_user)):
    """
    Поиск автомобилей по марке, модели или номерному знаку.
    """
    try:
        cars = search_cars(query)
        if not cars:
            return {"cars": [], "message": "No cars found matching the query."}
        return {"cars": cars, "user": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search cars: {str(e)}")


@router.post("/add_car/")
async def add_car_view(car: Car, user: str = Depends(get_current_user)):
    try:
        add_car(car)
        return {"message": f"Car added successfully by {user}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add car: {str(e)}")


@router.delete("/delete_car/{license_plate}")
async def delete_car_view(license_plate: str, user: str = Depends(get_current_user)):
    try:
        result = delete_car_by_license_plate(license_plate)
        if not result:
            raise HTTPException(status_code=404, detail="Car not found")
        return {"message": f"Car deleted successfully by {user}"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete car: {str(e)}")


@router.get("/get_cars/")
async def get_cars(user: str = Depends(get_current_user)):
    try:
        cars = get_all_cars()
        return {"cars": cars, "user": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve cars: {str(e)}")
