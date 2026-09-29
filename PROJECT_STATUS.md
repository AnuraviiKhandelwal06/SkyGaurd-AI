# SkyGuard Project Status

## 1. ML PIPELINE (skyguard/)
*   **Stage 1 (Edge QC)**: Exists (edge_qc.py). Real rule-based logic (range bounds, rate-of-change).
*   **Stage 2 (Temporal AI)**: Exists (	emporal_ai.py). Initializes a PyTorch LSTM Autoencoder (but does not load trained .pt weights) and has a Scikit-Learn Isolation Forest fallback.
*   **Stage 3 (Physics & Spatial)**: Exists (physics_spatial.py). 
*   **Stage 4 (Diagnosis)**: Exists (ault_classifier.py). 
*   **Stage 5 (Self-Healing)**: Exists (self_healing.py). 
*   **Stage 6 (Explainability)**: Exists (explainability.py). 
*   **Stage 7 (Health Intelligence)**: Exists (health_intelligence.py). 
*   **Called by backend?** 
    *   **Yes**, partially. The manual API route /api/ingest/{station_id} instantiates SkyGuardPipeline and processes the reading through all stages.
    *   **No**, for automated ingestion. The background poll_stations job in ingestion_service.py has the ML pipeline import commented out and uses simulated dummy logic (e.g., if temp > 45, inject Spike).
*   **test_pipeline_flow.py Output**:
    `	ext
    Forcing states via API with force_state param...
    AWS-001 (Genuine): NORMAL
    AWS-002 (Fault): NORMAL
    AWS-003 (Normal): NORMAL

    Waiting for DB to settle...

    Station    | DB Status    | API Status   | Correction?  | Rule Respected?
    --------------------------------------------------------------------------------
    AWS-001    | warning      | Warning      | No           | Yes
    AWS-002    | faulty       | Faulty       | Yes          | Yes
    AWS-003    | healthy      | Healthy      | No           | Yes
    `
*   **Known Unfixed ML Bugs**: "Two Simultaneous Spikes" spatial IDW flaw and "Recovering Sensor" rate-of-change flaw.

## 2. BACKEND (ackend/)
*   **API Routes**:
    *   /api/ingest/{station_id} (POST): Real data insertion, triggers real ML pipeline locally.
    *   /predict & /predict/all (GET): Real, fetches from DB.
    *   /{id}/decision (PATCH): Real, updates DB corrections.
    *   /api/dashboard/overview & /analytics/trends: Real DB aggregation queries.
*   **DB Row Counts**:
    *   stations: 5
    *   eadings: 231
    *   nomalies: 103
    *   corrections: 35
    *   sensor_health: 5
    *   ault_history: 40
*   **Ingestion Service**: Runs on a background schedule (every 5 mins via APScheduler in main.py). However, it **does not** call the ML pipeline. It uses simulated logic.
*   **Live Hardware Sensor**: **Stub**. PRIMARY_SENSOR_URL is hardcoded to "http://localhost:9999/api/sensor".

## 3. ML <-> BACKEND CONNECTION
*   **Trace (End to End)**:
    *   *Ingestion*: poll_stations queries localhost:9999 (fails/dummy data).
    *   *Pipeline*: Bypassed by background task, substituted with simulated anomaly creation.
    *   *DB Row (Actual Example)*: id: 231, station_id: AWS-003, 	emp: 11.74, humidity: 79.61, pressure: 990.82, nomaly_status: 'resolved'.
    *   *API Response*: Served successfully by /predict/all mapping DB records to JSON.

## 4. FRONTEND (rontend/)
*   **Pages**:
    *   dashboard.jsx: Uses real API (useStationsData).
    *   Livestations.jsx: Uses real API.
    *   nomalydetection.jsx: Uses real API.
    *   sensorhealth.jsx: Uses real API.
    *   settings.jsx: **Uses mock data** (imports mockdata.js).
*   **Components**:
    *   Indiamap.jsx: Uses real API.
    *   Livereadings.jsx: **BROKEN**. Expects stationsData prop, but dashboard.jsx does not pass it.
    *   RecentAlerts.jsx: **BROKEN**. Expects stationsData prop, but dashboard.jsx does not pass it.
*   **Dev Server**: 
pm run dev starts successfully without compile errors (ready in ~500ms).
*   **Recently Changed Files (Restore Attempt)**: dashboard.jsx, Livestations.jsx, nomalydetection.jsx, sensorhealth.jsx, Indiamap.jsx, pi.js, useStationsData.js, statusHelper.js.

## 5. KNOWN OPEN BUGS
*   **Warning vs Faulty Logic / Mismatch**: 
    *   *State*: The DB saves statuses as critical, warning, esolved. The frontend now has a statusHelper.js that maps critical -> Faulty and warning -> Warning. The Overview cards compute counts dynamically from the live data hook, resolving the previous numerical mismatch.
*   **Corrections exist only for Faulty?**: 
    *   *State*: **True**. Queried the DB: 35 corrections are linked exclusively to critical (Faulty) anomalies. warning and esolved anomalies have 0 corrections.

## 6. SUMMARY TABLE

| Component | Status | Evidence | What is needed to finish |
| :--- | :--- | :--- | :--- |
| **ML Pipeline** | Partial | 	est_pipeline_flow.py passes, but weights untrained. | Fix edge cases (Simultaneous Spikes). Load/train real PyTorch weights. |
| **Backend API** | Working | Routes return 200 OK and DB has hundreds of rows. | Remove dummy data gen; finalize actual schema mapping. |
| **Ingestion** | Broken / Mocked | ingestion_service.py ML call is commented out. | Integrate MQTT/BMP280 script; remove localhost:9999 stub. |
| **Frontend UI** | Partial | 
pm run dev works. Missing props crash components. | Pass props to Livereadings/RecentAlerts in dashboard.jsx; wire settings.jsx. |

## 7. RECOMMENDATION
**Fix the frontend in place.** Do NOT rebuild from scratch. The core architecture (useStationsData context and pi.js) is correctly wired to the real backend and DB. The only remaining frontend tasks are trivial prop-drilling fixes (<LiveReadings stationsData={stations} />) and migrating the Settings page off mock data. The rest of the effort should immediately pivot to Phase 1 (Live Hardware/MQTT Integration) and Phase 2 (ML Bugs).
