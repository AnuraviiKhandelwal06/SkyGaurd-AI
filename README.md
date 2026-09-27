# SkyGuard AI Backend

SkyGuard AI is an ML-based real-time anomaly detection system for Automatic Weather Stations. It analyzes temperature, pressure, and humidity to detect sensor faults, spikes, frozen values, and inconsistencies, providing alerts, confidence scores, root-cause analysis, sensor health, and optional data correction.

## Architecture
The backend is a FastAPI application that integrates directly with the SkyGuard ML pipeline. It uses PostgreSQL for storage.

```
Frontend -> FastAPI -> SkyGuard ML pipeline -> PostgreSQL -> API Responses
```

## Requirements
- Python 3.10+
- PostgreSQL
- Git

## Setup and Running (Windows PowerShell)

1. **Clone the repository:**
   ```powershell
   git clone <repository_url>
   cd SkyGaurd-AI
   ```

2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   python -m pip install -r requirements.txt
   ```

4. **Configure the Environment:**
   Copy `.env.example` to `.env` and configure your `DATABASE_URL`.
   ```powershell
   Copy-Item .env.example .env
   # Edit .env to match your PostgreSQL credentials
   # Example: DATABASE_URL=postgresql://postgres:password@localhost:5432/skyguard
   ```

5. **Start the application:**
   ```powershell
   python -m uvicorn app.main:app --reload
   ```
   *Note: During startup, the ML pipeline models (Torch, XGBoost, etc.) are initialized. This may take several seconds before the server is ready.*

## API Endpoints

Once running, access the interactive Swagger documentation at:
**http://localhost:8000/docs**

### Core Endpoints:
- `POST /api/sensor-data/upload`: Upload real-time telemetry (invokes ML pipeline).
- `GET /api/dashboard/overview`: Get network-wide health and active anomalies.
- `GET /api/stations`: List all registered stations.
- `GET /api/health/{station_code}`: View the AI-calculated health score of a station.
- `GET /api/anomalies/{station_code}`: View detected faults for a station.
