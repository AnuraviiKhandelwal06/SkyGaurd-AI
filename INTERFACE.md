# SkyGuard AI — Backend Engineering Integration Specification (`INTERFACE.md`)

This document defines the interface specification between the **SkyGuard AI Machine Learning Pipeline** (`skyguard/`) and the backend application service layer (FastAPI / Database / Dashboard).

---

## 1. Overview & Architecture Scope

SkyGuard AI is a physics-informed, temporal AI anomaly detection engine for Automatic Weather Stations (AWS). The core entry point `SkyGuardPipeline.process_reading()` processes hourly station telemetry in real time and evaluates physical bounds, temporal patterns, and multi-station spatial consensus.

---

## 2. Pipeline Initialization

```python
from skyguard.main_pipeline import SkyGuardPipeline
from skyguard.data.sources import MultiCSVSource

# Initialize spatial metadata for 4-station network
data_source = MultiCSVSource(data_dir=".")
station_metadata = data_source.get_station_metadata()

# Instantiate Pipeline
pipeline = SkyGuardPipeline(
    target_elevation_m=189.0,
    neighbor_metadata=station_metadata
)

# Pre-train pipeline on historical clean baseline (2010-2020)
train_clean_df = data_source.load_data()
pipeline.fit(train_clean_df)
```

---

## 3. Real-Time Ingestion Method (`process_reading`)

### Python Method Signature
```python
def process_reading(
    current_reading: Dict[str, Any],
    neighbor_readings: Optional[Dict[str, Dict[str, Any]]] = None
) -> Dict[str, Any]
```

---

## 4. Ground-Truth Actual Output Examples

Below are exact, real JSON outputs returned directly from `SkyGuardPipeline.process_reading()`:

### Example A: Actual Clean Reading JSON Output
```json
{
  "timestamp": "2023-01-01 00:00:00",
  "station_id": "TARGET_30_25N_74_25E",
  "is_anomaly": false,
  "anomaly_type": "CLEAN",
  "severity_score": 0.0,
  "confidence_score": 0.98,
  "diagnosis": {
    "diagnosis_type": "NORMAL",
    "root_cause": "Station operating within normal physical, temporal, and spatial bounds.",
    "evidence_chain": [
      "All edge, temporal, physics, and spatial checks passed clean."
    ]
  },
  "explainability": {
    "reason_string": "Station telemetry operating normally within expected physical, temporal, and spatial bounds.",
    "confidence_pct": 98.0,
    "shap_attributions": {
      "rate_temp": -0.0853,
      "rate_rh": -0.0934,
      "rate_press": -0.0756,
      "flatline_length": 0.0042,
      "missing_flag": 0.0,
      "lstm_mse": 0.1200,
      "iso_forest_score": 0.0829,
      "max_z_score": -0.1888,
      "hydrostatic_residual": 0.8396,
      "dew_point_deficit": 0.9436,
      "temp_spatial_z": 0.0,
      "rh_spatial_z": 0.0,
      "sp_spatial_z": 0.0,
      "spatial_agreement_ratio": 0.0
    }
  },
  "original_telemetry": {
    "temperature_2m": 7.1,
    "relative_humidity_2m": 91.0,
    "surface_pressure": 996.4,
    "pressure_msl": 1019.6
  },
  "corrected_telemetry": {
    "needs_correction": false,
    "temperature_2m": 7.1,
    "relative_humidity_2m": 91.0,
    "surface_pressure": 996.4,
    "pressure_msl": 1019.6,
    "reconstruction_confidence_pct": 100.0,
    "imputation_method": "PASSTHROUGH_ORIGINAL"
  },
  "sensor_health": {
    "health_score_pct": 99.7,
    "status": "Pristine - No maintenance required.",
    "predictive_maintenance_flag": false,
    "estimated_rul_days": 180,
    "recommended_action": "Routine 6-month calibration schedule active.",
    "sensor_breakdown": {
      "temperature_sensor_health_pct": 99.2,
      "humidity_sensor_health_pct": 99.7,
      "pressure_sensor_health_pct": 99.7
    },
    "rolling_7day_fault_rate_pct": 0.0
  },
  "evidence_metrics": {
    "edge_flags": {
      "range_violation": false,
      "rate_of_change_violation": false,
      "flatline_violation": false,
      "missing_data": false,
      "details": []
    },
    "temporal_lstm_mse": 0.01441,
    "physics_dew_point_c": 5.73,
    "hydrostatic_residual_hpa": 0.08,
    "spatial_expected_temp": 6.93,
    "spatial_temp_z_score": 0.22
  }
}
```

### Example B: Actual Anomalous Reading JSON Output (SPIKE Fault)
```json
{
  "timestamp": "2023-01-02 11:00:00",
  "station_id": "TARGET_30_25N_74_25E",
  "is_anomaly": true,
  "anomaly_type": "SPIKE",
  "severity_score": 7.5,
  "confidence_score": 0.95,
  "diagnosis": {
    "diagnosis_type": "SENSOR_FAULT",
    "root_cause": "Surface / MSL Pressure Sensor Calibration Drift.",
    "evidence_chain": [
      "Hydrostatic MSL-surface pressure delta deviates from station 189m elevation baseline."
    ]
  },
  "explainability": {
    "reason_string": "Flagged as SPIKE with 96.9% confidence due to 11.0°C/hr rate-of-change (exceeding 5.0°C/hr threshold) and spatial deviation (Z=0.9) from neighbor network.",
    "confidence_pct": 96.9,
    "shap_attributions": {
      "rate_temp": 0.3518,
      "rate_rh": 0.6009,
      "rate_press": -0.1390,
      "flatline_length": 0.1334,
      "missing_flag": 0.0,
      "lstm_mse": -0.0358,
      "iso_forest_score": -0.1823,
      "max_z_score": -0.1544,
      "hydrostatic_residual": 2.1155,
      "dew_point_deficit": 0.3096,
      "temp_spatial_z": 0.0,
      "rh_spatial_z": 0.0,
      "sp_spatial_z": 0.0,
      "spatial_agreement_ratio": 0.0
    }
  },
  "original_telemetry": {
    "temperature_2m": 18.1,
    "relative_humidity_2m": 40.0,
    "surface_pressure": 981.82,
    "pressure_msl": 1020.3
  },
  "corrected_telemetry": {
    "needs_correction": true,
    "temperature_2m": 13.6,
    "relative_humidity_2m": 67.4,
    "surface_pressure": 995.53,
    "pressure_msl": 1034.55,
    "reconstruction_confidence_pct": 94.5,
    "imputation_method": "DUAL_SPATIAL_TEMPORAL_IDW"
  },
  "sensor_health": {
    "health_score_pct": 0.0,
    "status": "Critical - High fault rate or hardware flatline/dropout.",
    "predictive_maintenance_flag": true,
    "estimated_rul_days": 2,
    "recommended_action": "IMMEDIATE ACTION REQUIRED: Replace sensor head module.",
    "sensor_breakdown": {
      "temperature_sensor_health_pct": 1.8,
      "humidity_sensor_health_pct": 0.0,
      "pressure_sensor_health_pct": 0.0
    },
    "rolling_7day_fault_rate_pct": 50.0
  },
  "evidence_metrics": {
    "edge_flags": {
      "range_violation": false,
      "rate_of_change_violation": true,
      "flatline_violation": false,
      "missing_data": false,
      "details": [
        "Temperature rate-of-change 11.0°C/hr exceeds threshold 5.0°C/hr.",
        "Humidity rate-of-change 51.0%/hr exceeds threshold 25.0%/hr.",
        "Pressure rate-of-change 14.6hPa/hr exceeds threshold 6.0hPa/hr."
      ]
    },
    "temporal_lstm_mse": 0.1676,
    "physics_dew_point_c": 4.28,
    "hydrostatic_residual_hpa": 16.42,
    "spatial_expected_temp": 17.1,
    "spatial_temp_z_score": 0.91
  }
}
```

---

## 5. Allowed `anomaly_type` Enum Reference

| Value | Type | Description |
| :--- | :--- | :--- |
| `"CLEAN"` | `string` | Station operating within normal bounds. |
| `"SPIKE"` | `string` | Sudden single-timestep sensor jump exceeding rate-of-change limit. |
| `"FROZEN"` | `string` | Sensor reading held statically constant ($N \ge 4\text{ hours}$). |
| `"DRIFT"` | `string` | Accumulating linear or exponential sensor calibration bias. |
| `"COMM_FAILURE"` | `string` | Missing NaN readings or signal dropout ($N \ge 2\text{ hours}$). |
| `"INCONSISTENT"` | `string` | Psychrometric dew point bound violation ($T_d > T$). |
| `"GENUINE_EXTREME"` | `string` | Multi-station confirmed meteorological storm/front (**Do Not Impute**). |
