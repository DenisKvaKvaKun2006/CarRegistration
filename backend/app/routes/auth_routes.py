from fastapi import APIRouter, HTTPException, Depends
from crud.auth_crud import register_user_crud, login_user_crud
from models.user import UserCreate, UserLogin
from security.jwt import decode_access_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/register")
async def register_user(user: UserCreate):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    try:
        return await register_user_crud(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login_user(user: UserLogin):
    try:
        return await login_user_crud(user)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"msg": f"Hello, {payload.get('sub')}!"}
