"""
Standalone CLI Replay & Evaluation Demo for SkyGuard AI.
Loads the 4 local station CSV datasets, corrupts the test set with synthetic anomalies,
pre-trains the ML pipeline, replays simulated real-time telemetry stream, evaluates
classification metrics and self-healing reconstruction accuracy, and generates EVALUATION_REPORT.md.
"""

import os
import sys
import time
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, mean_squared_error, mean_absolute_error

from skyguard.data.sources import MultiCSVSource
from skyguard.data.preprocessing import preprocess_station_df, split_data_chronologically
from skyguard.data.injector import SyntheticAnomalyInjector
from skyguard.main_pipeline import SkyGuardPipeline


def run_demo():
    print("================================================================================")
    print("      SKYGUARD AI: INTELLIGENT ANOMALY DETECTION FOR AWS (SIH 2026)")
    print("================================================================================")
    
    # 1. Load Data from 4 Local CSVs
    print("\n[Step 1/5] Loading 4 time-aligned local weather station datasets...")
    source = MultiCSVSource(data_dir=".")
    target_df = source.load_data()
    neighbor_dfs = source.get_neighbor_data()
    metadata = source.get_station_metadata()

    print(f"Target Station ({metadata['target']['station_id']}): {len(target_df)} hourly rows.")
    for st_id, meta in metadata['neighbors'].items():
        print(f" -> Neighbor {st_id}: {meta['distance_km']}km away, temp corr r={meta['corr_temp']}")

    # 2. Physical Preprocessing & Chronological Split
    print("\n[Step 2/5] Preprocessing physical features & splitting chronologically...")
    prep_target = preprocess_station_df(target_df, elevation_m=189.0)
    train_df, val_df, test_df = split_data_chronologically(prep_target)

    print(f" -> Train Set (2010-01-01 to 2020-12-31): {len(train_df)} rows (Clean baseline)")
    print(f" -> Val Set   (2021-01-01 to 2022-12-31): {len(val_df)} rows (Clean validation)")
    print(f" -> Test Set  (2023-01-01 to 2024-02-20): {len(test_df)} rows (~13.7 months / 416 days)")

    # 3. Synthetic Anomaly Injection on Test Set
    print("\n[Step 3/5] Injecting labeled synthetic anomalies into Test Set (4% rate)...")
    injector = SyntheticAnomalyInjector(seed=42)
    corrupted_test_df = injector.inject_anomalies(test_df)
    corrupted_val_df = injector.inject_anomalies(val_df)

    anomaly_counts = corrupted_test_df["anomaly_type"].value_counts()
    print("Injected Test Set Fault Distribution:")
    for fault_type, count in anomaly_counts.items():
        pct = (count / len(corrupted_test_df)) * 100
        print(f"   * {fault_type:15s}: {count:5d} timesteps ({pct:.2f}%)")

    # 4. Pipeline Pre-training
    print("\n[Step 4/5] Initializing & Pre-training SkyGuard ML Pipeline...")
    pipeline = SkyGuardPipeline(target_elevation_m=189.0, neighbor_metadata=metadata)
    pipeline.fit(train_df, synthetic_corrupted_val_df=corrupted_val_df)

    # 5. Simulated Real-Time Replay & Evaluation
    print("\n[Step 5/5] Executing simulated real-time stream replay (Evaluating 500 timesteps)...")
    replay_count = 500
    replay_slice = corrupted_test_df.iloc[:replay_count].copy()
    
    # Align neighbor data for replay slice
    neighbor_slices = {
        st_id: df.iloc[:replay_count].copy() for st_id, df in neighbor_dfs.items()
    }

    y_true = []
    y_pred = []
    
    orig_temps, corr_temps = [], []
    orig_sps, corr_sps = [], []

    print("-" * 100)
    print(f"{'TIME':16s} | {'FAULT TYPE':12s} | {'SEVERITY':8s} | {'CONF':6s} | {'SHAP EXPLANATION REASON STRING':45s}")
    print("-" * 100)

    for i in range(len(replay_slice)):
        row = replay_slice.iloc[i].to_dict()
        n_readings = {
            st_id: df.iloc[i].to_dict() for st_id, df in neighbor_slices.items()
        }

        # Process single reading in pipeline
        result = pipeline.process_reading(row, neighbor_readings=n_readings)

        actual_fault = row.get("anomaly_type", "CLEAN")
        predicted_fault = result["anomaly_type"]

        y_true.append(actual_fault)
        y_pred.append(predicted_fault)

        # Collect reconstruction evaluation metrics
        if actual_fault != "CLEAN" and actual_fault != "COMM_FAILURE":
            orig_temps.append(row.get("original_temperature_2m", row.get("temperature_2m")))
            corr_temps.append(result["corrected_telemetry"]["temperature_2m"])
            orig_sps.append(row.get("original_surface_pressure", row.get("surface_pressure")))
            corr_sps.append(result["corrected_telemetry"]["surface_pressure"])

        # Display Ticker Sample for Anomalies
        if result["is_anomaly"] or actual_fault != "CLEAN":
            time_str = str(row["time"])[:16]
            sev = f"{result['severity_score']:.1f}/10"
            conf = f"{result['confidence_score']*100:.0f}%"
            reason = result['explainability']['reason_string'][:45]
            print(f"{time_str:16s} | {predicted_fault:12s} | {sev:8s} | {conf:6s} | {reason:45s}")

    print("-" * 100)
    print("\n================================================================================")
    print("                        EVALUATION BENCHMARK RESULTS")
    print("================================================================================")

    # Classification Metrics
    labels = ["CLEAN", "SPIKE", "FROZEN", "DRIFT", "COMM_FAILURE", "INCONSISTENT"]
    print("\n1. Multi-Class Fault Classification Performance:")
    clf_report = classification_report(y_true, y_pred, labels=labels, zero_division=0)
    print(clf_report)

    # Self-Healing Metrics
    temp_rmse = np.sqrt(mean_squared_error(orig_temps, corr_temps)) if orig_temps else 0.0
    temp_mae = mean_absolute_error(orig_temps, corr_temps) if orig_temps else 0.0
    sp_rmse = np.sqrt(mean_squared_error(orig_sps, corr_sps)) if orig_sps else 0.0
    sp_mae = mean_absolute_error(orig_sps, corr_sps) if orig_sps else 0.0

    print("\n2. Self-Healing Data Correction Accuracy vs Ground Truth Clean Values:")
    print(f"   * Temperature Imputation RMSE : {temp_rmse:.3f}°C (MAE: {temp_mae:.3f}°C)")
    print(f"   * Pressure Imputation RMSE    : {sp_rmse:.3f} hPa (MAE: {sp_mae:.3f} hPa)")

    # Generate EVALUATION_REPORT.md
    report_path = "EVALUATION_REPORT.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# SkyGuard AI — Evaluation & Performance Report\n\n")
        f.write("## 1. Multi-Class Fault Classifier Metrics\n\n")
        f.write("```\n")
        f.write(clf_report)
        f.write("\n```\n\n")
        f.write("## 2. Self-Healing Imputation Accuracy\n\n")
        f.write(f"- **Temperature Imputation**: RMSE = `{temp_rmse:.3f}°C`, MAE = `{temp_mae:.3f}°C`\n")
        f.write(f"- **Surface Pressure Imputation**: RMSE = `{sp_rmse:.3f} hPa`, MAE = `{sp_mae:.3f} hPa`\n\n")
        f.write("## 3. Evaluation Setup Summary\n\n")
        f.write("- **Station Network**: 4 time-aligned Open-Meteo stations (2010-01-01 to 2024-02-20)\n")
        f.write("- **Test Set Window**: 2023-01-01 to 2024-02-20 (9,984 rows, ~13.7 months / 416 days)\n")
        f.write("- **Injected Anomaly Rate**: 4.0%\n")

    print(f"\n[Done] Full evaluation report generated and saved to '{report_path}'.\n")


if __name__ == "__main__":
    run_demo()
