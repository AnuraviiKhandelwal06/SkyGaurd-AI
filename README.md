# 🛡️ SkyGuard AI

**Intelligent Weather Station Monitoring & Anomaly Detection System**

SkyGuard AI is an end-to-end platform for monitoring weather stations across India, detecting sensor anomalies using machine learning, and providing actionable insights through an interactive dashboard.

## 📁 Project Structure

```
├── backend/          # FastAPI backend (REST API, database, ML integration)
├── frontend/         # React + Vite frontend (dashboard, maps, charts)
├── skyguard/         # ML pipeline module (anomaly detection, fault classification)
├── ml-development/   # ML development & evaluation scripts
├── Dockerfile        # Docker config for Render deployment
└── render.yaml       # Render Blueprint (Infrastructure as Code)
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+**
- **Node.js 18+**
- **PostgreSQL** (local dev) or use the Render free tier

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
pip install -r ../ml-development/requirements.txt
cp .env.example .env            # Edit with your DATABASE_URL
alembic upgrade head
uvicorn app.main:app --reload --port 8080
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env            # Edit API URL if needed
npm run dev
```

## ☁️ Deployment

### Frontend → Vercel

1. Push to GitHub
2. Import the repo on [Vercel](https://vercel.com)
3. Set **Root Directory** to `frontend`
4. Framework: **Vite**
5. Add env var `VITE_API_URL` = your Render backend URL

### Backend → Render

1. Push to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. **New → Blueprint** → connect your repo
4. Render reads `render.yaml` and provisions everything automatically
5. Or manually: **New → Web Service** → Docker → set environment variables

### Environment Variables

| Variable | Where | Description |
|---|---|---|
| `DATABASE_URL` | Render | PostgreSQL connection string (auto-set by Render) |
| `FRONTEND_URL` | Render | Your Vercel frontend URL (for CORS) |
| `VITE_API_URL` | Vercel | Your Render backend URL |
| `VITE_DATA_MODE` | Vercel | `static` (demo) or `api` (live) |

## 🧠 ML Pipeline

The `skyguard` module provides:

- **Temporal AI** – time-series anomaly detection
- **Physics-Spatial Validation** – cross-station spatial checks
- **Fault Classification** – XGBoost-based sensor fault typing
- **Explainability** – SHAP-based feature attribution
- **Self-Healing** – automated correction suggestions

## 📄 License

This project was built for SIH (Smart India Hackathon).
