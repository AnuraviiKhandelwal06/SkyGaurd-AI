from fastapi import FastAPI

from app.core.database import engine, Base

from app.api.routes.stations import router as stations_router
from app.api.routes.readings import router as readings_router
from app.api.routes.health import router as health_router
from app.api.routes.anomalies import router as anomalies_router

# Import models so SQLAlchemy registers their tables
from app.models.sensor_health import SensorHealth
from app.models.anomaly import Anomaly


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="SkyGuard AI API"
)


# Register API routes
app.include_router(stations_router)
app.include_router(readings_router)
app.include_router(health_router)
app.include_router(anomalies_router)


@app.get("/")
def home():
    return {
        "message": "SkyGuard AI Backend is running"
    }