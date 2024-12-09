from database import users_collection
from models.user import UserCreate, UserLogin
from security.hashing import hash_password, verify_password
from security.jwt import create_access_token


async def register_user_crud(user: UserCreate):
    print({"email": user.email})
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise ValueError("Email already registered")

    hashed_password = hash_password(user.password)
    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "hashed_password": hashed_password
    }

    users_collection.insert_one(user_data)
    return {"msg": "User registered successfully"}


async def login_user_crud(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise ValueError("Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
