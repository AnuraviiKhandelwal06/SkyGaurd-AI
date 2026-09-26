"""
Synthetic Anomaly Injection Module for SkyGuard AI.
Corrupts clean weather telemetry with labeled fault types for training and evaluating
anomaly detection, multi-class fault classification, explainability, and self-healing algorithms.
"""

from typing import Tuple, Dict, List
import pandas as pd
import numpy as np


class SyntheticAnomalyInjector:
    """
    Injects realistic AWS sensor faults into clean weather time series data:
    1. Spike (Single-step jump beyond rate of change threshold)
    2. Frozen Value (Stuck constant value for N hours)
    3. Drift (Accumulating linear bias over N hours)
    4. Communication Failure (NaN / null value dropouts)
    5. Cross-Parameter Inconsistency (Psychrometric dew point violations)
    """

    def __init__(self, seed: int = 42):
        self.seed = seed

    def inject_anomalies(
        self,
        df: pd.DataFrame,
        injection_rates: Dict[str, float] = None
    ) -> pd.DataFrame:
        """
        Injects anomalies into target columns and retains uncorrupted values for evaluation.
        """
        if injection_rates is None:
            injection_rates = {
                "SPIKE": 0.010,
                "FROZEN": 0.008,
                "DRIFT": 0.008,
                "COMM_FAILURE": 0.008,
                "INCONSISTENT": 0.006,
            }

        np.random.seed(self.seed)
        corrupted_df = df.copy()

        # Save ground truth clean signals
        for col in ["temperature_2m", "relative_humidity_2m", "surface_pressure", "pressure_msl"]:
            corrupted_df[f"original_{col}"] = corrupted_df[col]

        corrupted_df["is_anomaly"] = 0
        corrupted_df["anomaly_type"] = "CLEAN"

        n_rows = len(corrupted_df)
        cols_to_corrupt = ["temperature_2m", "relative_humidity_2m", "surface_pressure", "pressure_msl"]

        # Track occupied time ranges to avoid overlapping injections
        occupied = np.zeros(n_rows, dtype=bool)

        # 1. SPIKE
        n_spikes = int(n_rows * injection_rates.get("SPIKE", 0.01))
        spike_indices = np.random.choice(np.where(~occupied)[0], size=min(n_spikes, np.sum(~occupied)), replace=False)
        for idx in spike_indices:
            occupied[idx] = True
            var = np.random.choice(["temperature_2m", "relative_humidity_2m", "surface_pressure"])
            sign = np.random.choice([-1, 1])
            if var == "temperature_2m":
                magnitude = sign * np.random.uniform(8.0, 20.0)
            elif var == "relative_humidity_2m":
                magnitude = sign * np.random.uniform(30.0, 60.0)
            else:
                magnitude = sign * np.random.uniform(15.0, 40.0)

            corrupted_df.loc[idx, var] += magnitude
            if var == "relative_humidity_2m":
                corrupted_df.loc[idx, var] = np.clip(corrupted_df.loc[idx, var], 0.0, 100.0)
            corrupted_df.loc[idx, "is_anomaly"] = 1
            corrupted_df.loc[idx, "anomaly_type"] = "SPIKE"

        # 2. FROZEN VALUE
        n_frozen_events = int(n_rows * injection_rates.get("FROZEN", 0.008) / 10)
        for _ in range(n_frozen_events):
            duration = np.random.randint(4, 24)
            valid_starts = np.where(~occupied[:-duration])[0]
            if len(valid_starts) == 0:
                break
            start_idx = np.random.choice(valid_starts)
            var = np.random.choice(["temperature_2m", "relative_humidity_2m", "surface_pressure"])
            stuck_value = corrupted_df.loc[start_idx, var]

            for t in range(start_idx, start_idx + duration):
                occupied[t] = True
                corrupted_df.loc[t, var] = stuck_value
                corrupted_df.loc[t, "is_anomaly"] = 1
                corrupted_df.loc[t, "anomaly_type"] = "FROZEN"

        # 3. DRIFT
        n_drift_events = int(n_rows * injection_rates.get("DRIFT", 0.008) / 24)
        for _ in range(n_drift_events):
            duration = np.random.randint(12, 72)
            valid_starts = np.where(~occupied[:-duration])[0]
            if len(valid_starts) == 0:
                break
            start_idx = np.random.choice(valid_starts)
            var = np.random.choice(["temperature_2m", "surface_pressure"])
            total_bias = np.random.choice([-1, 1]) * np.random.uniform(3.0, 8.0)
            drift_step = total_bias / duration

            for i, t in enumerate(range(start_idx, start_idx + duration)):
                occupied[t] = True
                bias = drift_step * (i + 1)
                corrupted_df.loc[t, var] += bias
                if var == "surface_pressure":
                    corrupted_df.loc[t, "pressure_msl"] += bias
                corrupted_df.loc[t, "is_anomaly"] = 1
                corrupted_df.loc[t, "anomaly_type"] = "DRIFT"

        # 4. COMMUNICATION FAILURE / MISSING DATA
        n_comm_events = int(n_rows * injection_rates.get("COMM_FAILURE", 0.008) / 6)
        for _ in range(n_comm_events):
            duration = np.random.randint(2, 12)
            valid_starts = np.where(~occupied[:-duration])[0]
            if len(valid_starts) == 0:
                break
            start_idx = np.random.choice(valid_starts)
            for t in range(start_idx, start_idx + duration):
                occupied[t] = True
                for col in cols_to_corrupt:
                    corrupted_df.loc[t, col] = np.nan
                corrupted_df.loc[t, "is_anomaly"] = 1
                corrupted_df.loc[t, "anomaly_type"] = "COMM_FAILURE"

        # 5. CROSS-PARAMETER INCONSISTENCY
        n_inconsistent = int(n_rows * injection_rates.get("INCONSISTENT", 0.006))
        valid_starts = np.where(~occupied)[0]
        if len(valid_starts) > 0:
            inc_indices = np.random.choice(valid_starts, size=min(n_inconsistent, len(valid_starts)), replace=False)
            for idx in inc_indices:
                occupied[idx] = True
                # Force high temp + impossible high RH without precipitation/fog conditions
                corrupted_df.loc[idx, "temperature_2m"] = 42.0
                corrupted_df.loc[idx, "relative_humidity_2m"] = 98.0 # Yields DewPoint > 41°C (physically extreme)
                corrupted_df.loc[idx, "is_anomaly"] = 1
                corrupted_df.loc[idx, "anomaly_type"] = "INCONSISTENT"

        return corrupted_df
