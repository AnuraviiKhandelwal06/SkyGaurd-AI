from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.routes.stations import router as stations_router
from app.api.routes.readings import router as readings_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SkyGuard AI API")

app.include_router(stations_router)
app.include_router(readings_router)


@app.get("/")
def home():
    return {"message": "SkyGuard AI Backend is running"}    