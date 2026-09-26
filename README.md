# SkyGuard AI — Intelligent Anomaly Detection for AWS

**Team**: Cipher | **SIH 2026** | **PS ID**: 26073 | **Theme**: Disaster Management

SkyGuard AI is a multi-layered, physics-informed, temporal AI anomaly detection, diagnosis, explainability, self-healing, and predictive maintenance framework designed for Automatic Weather Stations (AWS).

It ingests hourly weather streams consisting of **Temperature (°C)**, **Relative Humidity (%)**, **Surface Pressure (hPa)**, and **MSL Pressure (hPa)** to detect sensor corruptions in real time and distinguish them from genuine meteorological extreme weather events.

---

## 1. Real 4-Station Network Topology

The system evaluates physical, temporal, and spatial consensus across **4 time-aligned local station datasets** (`2010-01-01` to `2024-02-20`, 123,936 hourly rows each):

| Station Role | File Name | Coordinates | Elevation | Distance | Temp Correlation ($r$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Target AWS** | `open-meteo-30_25N74_25E189m.csv` | 30.25°N, 74.25°E | 189m | 0 km | 1.000 |
| **Neighbor 1** | `open-meteo-30_69N74_82E212m.csv` | 30.69°N, 74.82°E | 212m | ~65 km | **0.981** |
| **Neighbor 2** | `open-meteo-29_00N75_03E199m.csv` | 29.00°N, 75.03°E | 199m | ~150 km | **0.975** |
| **Neighbor 3** | `open-meteo-28_58N77_19E224m.csv` | 28.58°N, 77.19°E | 224m | ~330 km | **0.960** |

---

## 2. 8-Stage Architecture Pipeline

1. **Stage 1: Real-Time Edge QC** — Lightweight rule-based check for physical range bounds ($T \in [-10, 55]^\circ\text{C}$), rate of change ($>5^\circ\text{C/hr}$), flatline ($N \ge 4\text{ hours}$), and missing NaN dropouts.
2. **Stage 2: Temporal AI Engine** — PyTorch LSTM Autoencoder sequence-to-sequence model ($W=24\text{h}$) + Isolation Forest & Rolling Z-Score baselines.
3. **Stage 3: Physics + Distance-Weighted Spatial Engine** — Psychrometric Dew Point bound ($T_d \le T$), Hydrostatic MSL-surface pressure elevation residual, and Inverse Distance Weighting (IDW) spatial consensus across neighbors.
4. **Stage 4: Counterfactual Diagnosis** — Fuses evidence across Edge, Temporal, Physics, and Spatial layers to disambiguate **Sensor Faults** from **Genuine Extreme Weather Events**.
5. **Stage 5: Multi-Class Fault Classifier** — XGBoost multi-class classifier trained over 14 physical/temporal/spatial features (`SPIKE`, `FROZEN`, `DRIFT`, `COMM_FAILURE`, `INCONSISTENT`, `GENUINE_EXTREME`).
6. **Stage 6: Explainability (SHAP)** — SHAP attributions surfaced as human-readable natural language reason strings.
7. **Stage 7: Self-Healing / Data Correction** — Dual Spatial IDW + 48-hour Temporal Ridge Regression imputation with reconstruction confidence (%).
8. **Stage 8: Sensor Health Intelligence** — Rolling 7-day health score ($0-100\%$), Remaining Useful Life (RUL in days), and predictive maintenance action flags.

---

## 3. Directory Structure

```
ML SKYGUARD-AI/
├── open-meteo-30_25N74_25E189m.csv     # Target AWS Dataset (2010-2024, 123,936 rows)
├── open-meteo-30_69N74_82E212m.csv     # Neighbor 1 Dataset (~65km)
├── open-meteo-29_00N75_03E199m.csv     # Neighbor 2 Dataset (~150km)
├── open-meteo-28_58N77_19E224m.csv     # Neighbor 3 Dataset (~330km)
├── skyguard/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── injector.py                 # Synthetic Anomaly Injector module
│   │   ├── preprocessing.py            # Hydrostatic pressure delta, dew point, chronological train/val/test split
│   │   └── sources.py                  # MultiCSVSource, WeatherDataSource, SyntheticNeighborSource
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── counterfactual.py           # Stage 4: Multi-Evidence Counterfactual Diagnosis
│   │   ├── edge_qc.py                  # Stage 1: Edge QC Rules
│   │   ├── explainability.py           # Stage 6: SHAP Explainability & Reason Strings
│   │   ├── fault_classifier.py         # Stage 5: Multi-Class XGBoost Fault Classifier
│   │   ├── health_intelligence.py      # Stage 8: Sensor Health Index & Predictive Maintenance
│   │   ├── physics_spatial.py          # Stage 3: Psychrometrics, Hydrostatic Delta, IDW Spatial Consensus
│   │   ├── self_healing.py             # Stage 7: Dual Spatial IDW + Temporal Imputation
│   │   └── temporal_ai.py              # Stage 2: PyTorch LSTM Autoencoder & IsolationForest
│   └── main_pipeline.py                # SkyGuardPipeline master entry point (process_reading())
├── demo_replay.py                      # CLI Batch Replay & Stream Simulator
├── evaluate_full_test_set.py           # Benchmark script over full 9,984 test timesteps
├── INTERFACE.md                        # Backend Integration Specification Contract
├── EVALUATION_REPORT.md                # Quantitative Evaluation Metrics & Latency Benchmark
├── requirements.txt                    # Pinned package dependencies
├── .gitignore                          # Standard Python ML repository ignore rules
└── README.md                           # Master project documentation
```

---

## 4. Output Demonstration: Disambiguating SPIKE vs. GENUINE_EXTREME

A core strength of SkyGuard AI is distinguishing between an isolated **Sensor Spike** (where the target jump is unconfirmed by spatial neighbors) and a **Genuine Extreme Event** (where a rapid rate change is validated by spatial neighbor consensus):

### Isolated Sensor Spike Fault (`SPIKE`)
```json
{
  "timestamp": "2023-01-21 20:00:00",
  "station_id": "TARGET_30_25N_74_25E",
  "is_anomaly": true,
  "anomaly_type": "SPIKE",
  "severity_score": 6.0,
  "confidence_score": 0.98,
  "diagnosis": {
    "diagnosis_type": "SENSOR_FAULT",
    "root_cause": "Isolated Sensor Spike Fault (Abrupt rate-of-change jump).",
    "evidence_chain": [
      "Rate-of-change violation: temperature jump 10.0°C/hr exceeds 5.0°C/hr threshold.",
      "Unconfirmed by spatial neighbors (Spatial Z-score = 4.2 > 3.0)."
    ]
  },
  "explainability": {
    "reason_string": "Flagged as SPIKE with 98.0% confidence due to isolated 10.0°C/hr temperature rate-of-change (exceeding 5.0°C/hr threshold) unconfirmed by neighbor network (spatial consensus Z=4.2 > 3.0).",
    "confidence_pct": 98.0
  },
  "corrected_telemetry": {
    "needs_correction": true,
    "temperature_2m": 10.96,
    "reconstruction_confidence_pct": 94.5,
    "imputation_method": "DUAL_SPATIAL_TEMPORAL_IDW"
  }
}
```

### Genuine Meteorological Extreme Event (`GENUINE_EXTREME`)
```json
{
  "timestamp": "2023-01-21 20:00:00",
  "station_id": "TARGET_30_25N_74_25E",
  "is_anomaly": true,
  "anomaly_type": "GENUINE_EXTREME",
  "severity_score": 3.5,
  "confidence_score": 0.92,
  "diagnosis": {
    "diagnosis_type": "GENUINE_EXTREME_EVENT",
    "root_cause": "Genuine Extreme Meteorological Event confirmed by spatial neighbor consensus.",
    "evidence_chain": [
      "Rapid temperature drop matched by spatial consensus across neighbor network."
    ]
  },
  "explainability": {
    "reason_string": "Flagged as GENUINE_EXTREME with 92.0% confidence due to rapid meteorological rate change validated by high spatial consensus across neighbor network.",
    "confidence_pct": 92.0
  },
  "corrected_telemetry": {
    "needs_correction": false,
    "temperature_2m": 8.0,
    "reconstruction_confidence_pct": 100.0,
    "imputation_method": "PASS_THROUGH"
  }
}
```

---

## 5. Execution & Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Run Standalone Replay & Stream Simulator
```bash
python demo_replay.py
```

### Run Full Test Set Benchmark (9,984 Rows)
```bash
python evaluate_full_test_set.py
```

---

## 6. Backend Integration Contract

For web application, API, and cloud backend integration, inspect [`INTERFACE.md`](file:///c:/Users/EliteBook/OneDrive/Desktop/ML%20SKYGUARD-AI/INTERFACE.md), which defines:
- Mandatory input dictionary keys per stream reading (`timestamp`, `temperature_2m`, `relative_humidity_2m`, `surface_pressure`, `pressure_msl`, and spatial `neighbor_readings`).
- Full standard JSON response payload schema produced by `process_reading()`.

---

## 7. Deterministic Reproducibility

Random seeds are explicitly locked across all stochastic components (`SEED = 42`):
- PyTorch: `torch.manual_seed(42)`
- NumPy: `np.random.seed(42)`
- XGBoost: `XGBClassifier(random_state=42)`
- Isolation Forest: `IsolationForest(random_state=42)`
- Synthetic Anomaly Injector: `SyntheticAnomalyInjector(seed=42)`

Executing two sequential runs of `evaluate_full_test_set.py` produces **100.0% bit-identical metrics** across all 9,984 test timesteps:
- **Accuracy**: `0.9068`
- **Weighted Precision**: `0.9687`
- **Weighted Recall**: `0.9068`
- **Weighted F1-Score**: `0.9360`

---

## 8. Scaling to Large AWS Networks ($N > 4$ Stations)

To scale SkyGuard AI to a network of $N$ AWS stations:
1. Load neighbor datasets using `MultiCSVSource` or `SyntheticNeighborSource`.
2. Provide station coordinates (`lat`, `lon`, `elevation`) in the spatial metadata dictionary.
3. Stage 3 automatically calculates distance degradation weights:
   $$w_i = \frac{r_i / d_i}{\sum_{j=1}^N (r_j / d_j)}$$
4. Pipeline detection, classification, and self-healing modules operate seamlessly without code changes.
