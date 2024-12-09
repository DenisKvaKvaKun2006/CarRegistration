from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from routes import car_routes, registration_routes, auth_routes
from database import users_collection
import os

app = FastAPI()

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(car_routes.router, prefix="/carsdb", tags=["carsdb"])
app.include_router(registration_routes.router, prefix="/regdb", tags=["regdb"])
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(open(os.path.join("frontend", "html", "index.html")).read())
