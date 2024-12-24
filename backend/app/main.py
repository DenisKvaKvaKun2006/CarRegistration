import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from routes import car_routes, registration_routes, auth_routes

app: FastAPI = FastAPI()

# Разрешенные источники для CORS
origins: list[str] = [
    "http://127.0.0.1:8000",
    "http://localhost:8000"
]

# Добавление промежуточного слоя для обработки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(
    car_routes.router,
    prefix="/carsdb",
    tags=["carsdb"]
)
app.include_router(
    registration_routes.router,
    prefix="/regdb",
    tags=["regdb"]
)
app.include_router(
    auth_routes.router,
    prefix="/auth",
    tags=["auth"]
)

# Подключение статических файлов
app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)


@app.get("/", response_class=HTMLResponse)
async def read_root() -> HTMLResponse:
    """
    Обработчик для корневого маршрута.

    Returns:
        HTMLResponse: Содержимое HTML-файла главной страницы.
    """
    index_path: str = os.path.join("frontend", "html", "index.html")
    try:
        with open(index_path, "r", encoding="utf-8") as html_file:
            content: str = html_file.read()
        return HTMLResponse(content)
    except FileNotFoundError:
        return HTMLResponse(
            content="Главная HTML-страница не найдена.",
            status_code=404
        )
