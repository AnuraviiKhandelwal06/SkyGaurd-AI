"""
Data preprocessing, physical feature engineering, and temporal split module for SkyGuard AI.
Handles hydrostatic pressure calculations, dew point derivation, and time-based train/val/test splits.
"""

from typing import Tuple, Dict
import pandas as pd
import numpy as np


def compute_dew_point(temp_c: np.ndarray, rh_pct: np.ndarray) -> np.ndarray:
    """
    Computes Dew Point Temperature (°C) using Magnus-Tetens approximation.
    Valid for temp in [-45°C, 60°C] and RH in [1%, 100%].
    """
    rh_clipped = np.clip(rh_pct, 0.1, 100.0)
    a, b = 17.625, 243.04
    gamma = (a * temp_c) / (b + temp_c) + np.log(rh_clipped / 100.0)
    dew_point = (b * gamma) / (a - gamma)
    return dew_point


def compute_theoretical_hydrostatic_delta(surface_pressure_hpa: np.ndarray, temp_c: np.ndarray, elevation_m: float = 189.0) -> np.ndarray:
    """
    Computes theoretical MSL - Surface pressure delta (hPa) for a given station elevation
    using the barometric hydrostatic formula:
    P_msl = P_surface * (1 - 0.0065 * h / (T_c + 273.15)) ^ (-5.257)
    """
    temp_k = temp_c + 273.15
    lapse_term = 1.0 - (0.0065 * elevation_m) / temp_k
    msl_theoretical = surface_pressure_hpa * (lapse_term ** -5.257)
    theoretical_delta = msl_theoretical - surface_pressure_hpa
    return theoretical_delta


def preprocess_station_df(df: pd.DataFrame, elevation_m: float = 189.0) -> pd.DataFrame:
    """
    Adds derived physical features to station DataFrame:
    - pressure_delta: actual (pressure_msl - surface_pressure)
    - theoretical_p_delta: expected hydrostatic pressure delta
    - hydrostatic_residual: |actual_delta - theoretical_delta|
    - dew_point: derived dew point temperature (°C)
    - dew_point_deficit: temp_c - dew_point (must be >= -0.5°C in physical reality)
    """
    df = df.copy()
    df["time"] = pd.to_datetime(df["time"])
    
    temp = df["temperature_2m"].values
    rh = df["relative_humidity_2m"].values
    sp = df["surface_pressure"].values
    msl = df["pressure_msl"].values

    df["pressure_delta"] = msl - sp
    df["theoretical_p_delta"] = compute_theoretical_hydrostatic_delta(sp, temp, elevation_m)
    df["hydrostatic_residual"] = np.abs(df["pressure_delta"] - df["theoretical_p_delta"])
    
    dew_pt = compute_dew_point(temp, rh)
    df["dew_point"] = dew_pt
    df["dew_point_deficit"] = temp - dew_pt
    
    return df


def split_data_chronologically(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Splits DataFrame strictly by timestamp (No Data Leakage):
    - Train: 2010-01-01 to 2020-12-31 (11 years, 96,432 rows)
    - Val:   2021-01-01 to 2022-12-31 (2 years, 17,520 rows)
    - Test:  2023-01-01 to 2024-02-20 (~13.7 months / 416 days, 9,984 rows)
    """
    df = df.sort_values("time").reset_index(drop=True)
    
    train_mask = df["time"] <= "2020-12-31 23:00:00"
    val_mask = (df["time"] >= "2021-01-01 00:00:00") & (df["time"] <= "2022-12-31 23:00:00")
    test_mask = df["time"] >= "2023-01-01 00:00:00"

    train_df = df[train_mask].copy().reset_index(drop=True)
    val_df = df[val_mask].copy().reset_index(drop=True)
    test_df = df[test_mask].copy().reset_index(drop=True)

    return train_df, val_df, test_df
