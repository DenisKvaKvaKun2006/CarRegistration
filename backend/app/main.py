from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from routes import car_routes, registration_routes
import os

app = FastAPI()

app.include_router(car_routes.router)
app.include_router(registration_routes.router)
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(open(os.path.join("frontend", "html", "index.html")).read())
