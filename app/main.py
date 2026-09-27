from fastapi import FastAPI

from app.core.database import engine, Base

from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.stations import router as stations_router
from app.api.routes.readings import router as readings_router
from app.api.routes.health import router as health_router
from app.api.routes.anomalies import router as anomalies_router

# Import models so SQLAlchemy registers their tables
from app.models.sensor_health import SensorHealth
from app.models.anomaly import Anomaly


# Create database tables
Base.metadata.create_all(bind=engine)


from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize ML pipeline here
    from app.services.ml_service import init_ml_pipeline
    init_ml_pipeline()
    yield
    # Shutdown

app = FastAPI(
    title="SkyGuard AI API",
    lifespan=lifespan
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(stations_router)
app.include_router(readings_router)
app.include_router(health_router)
app.include_router(anomalies_router)
app.include_router(dashboard_router)


@app.get("/")
def home():
    return {
        "message": "SkyGuard AI Backend is running"
    }