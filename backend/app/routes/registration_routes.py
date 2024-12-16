from fastapi import APIRouter, Depends, HTTPException
from models.registration import Registration
from crud.registration_crud import add_registration, get_all_registrations, delete_registration_by_license_plate, \
    search_registrations, update_registration_by_license_plate
from security.jwt import decode_access_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload.get("sub")


router = APIRouter()


@router.put("/update_registration/{license_plate}")
async def update_registration_view(license_plate: str, update_data: dict, user: str = Depends(get_current_user)):
    """
    Редактировать данные регистрации. Номер автомобиля редактировать запрещено.
    """
    try:
        updated = update_registration_by_license_plate(license_plate, update_data)
        if not updated:
            raise HTTPException(status_code=404, detail="Registration not found or no updates applied")
        return {"message": f"Registration updated successfully by {user}"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update registration: {str(e)}")



@router.get("/search_registrations/")
async def search_registrations_view(query: str, user: str = Depends(get_current_user)):
    """
    Поиск регистраций по номеру автомобиля, имени владельца и адресу.
    """
    try:
        registrations = search_registrations(query)
        if not registrations:
            return {"registrations": [], "message": "No registrations found matching the query."}
        return {"registrations": registrations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search registrations: {str(e)}")


@router.post("/add_registration/")
async def add_registration_view(registration: Registration, user: str = Depends(get_current_user)):
    try:
        add_registration(registration)
        return {"message": f"Registration added successfully by {user}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add registration: {str(e)}")


@router.get("/get_registrations/")
async def get_registrations(user: str = Depends(get_current_user)):
    try:
        registrations = get_all_registrations()
        return {"registrations": registrations, "user": user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve registrations: {str(e)}")


@router.delete("/delete_registration/{license_plate}")
async def delete_registration(license_plate: str, user: str = Depends(get_current_user)):
    try:
        result = delete_registration_by_license_plate(license_plate)
        if not result:
            raise HTTPException(status_code=404, detail="Registration not found")
        return {"message": f"Registration deleted successfully by {user}"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete registration: {str(e)}")
