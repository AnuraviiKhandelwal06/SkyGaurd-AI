"""
Data Source Interface and Implementations for SkyGuard AI.
Supports MultiCSVSource (default real 4-station local dataset),
SyntheticNeighborSource (for scaling network simulations),
and OpenMeteoAPISource (for live REST API integration).
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional
import os
import pandas as pd
import numpy as np


class WeatherDataSource(ABC):
    """Abstract interface for fetching station telemetry and spatial neighbor evidence."""

    @abstractmethod
    def load_data(self) -> pd.DataFrame:
        """Loads and returns target station DataFrame with time index."""
        pass

    @abstractmethod
    def get_neighbor_data(self) -> Dict[str, pd.DataFrame]:
        """Returns dict mapping station_id -> DataFrame of neighbor readings."""
        pass

    @abstractmethod
    def get_station_metadata(self) -> Dict[str, Dict]:
        """Returns metadata (lat, lon, elevation, distance_km, correlation) for target and neighbors."""
        pass


class MultiCSVSource(WeatherDataSource):
    """
    Primary data source using 4 time-aligned real Open-Meteo station CSV files.
    - Target: open-meteo-30_25N74_25E189m.csv (AWS monitored)
    - Neighbor 1: open-meteo-30_69N74_82E212m.csv (~65km away, r=0.981/0.993)
    - Neighbor 2: open-meteo-29_00N75_03E199m.csv (~150km away, r=0.975/0.981)
    - Neighbor 3: open-meteo-28_58N77_19E224m.csv (~330km away, r=0.960/0.973)
    """

    def __init__(self, data_dir: str = "."):
        self.data_dir = data_dir
        self.target_file = os.path.join(data_dir, "open-meteo-30_25N74_25E189m.csv")
        self.neighbor_files = {
            "STATION_30_69N_74_82E": {
                "path": os.path.join(data_dir, "open-meteo-30_69N74_82E212m.csv"),
                "lat": 30.69, "lon": 74.82, "elevation": 212, "distance_km": 65.0, "corr_temp": 0.981
            },
            "STATION_29_00N_75_03E": {
                "path": os.path.join(data_dir, "open-meteo-29_00N75_03E199m.csv"),
                "lat": 29.00, "lon": 75.03, "elevation": 199, "distance_km": 150.0, "corr_temp": 0.975
            },
            "STATION_28_58N_77_19E": {
                "path": os.path.join(data_dir, "open-meteo-28_58N77_19E224m.csv"),
                "lat": 28.58, "lon": 77.19, "elevation": 224, "distance_km": 330.0, "corr_temp": 0.960
            },
        }
        self.target_metadata = {
            "station_id": "TARGET_30_25N_74_25E",
            "lat": 30.25, "lon": 74.25, "elevation": 189, "distance_km": 0.0, "corr_temp": 1.0
        }
        self._target_df = None
        self._neighbor_dfs = {}

    def _read_csv_file(self, filepath: str) -> pd.DataFrame:
        """Safely reads CSV file handling potential comment headers or clean schema."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Required station CSV file not found: {filepath}")
        
        # Check if first line contains comment or header
        df = pd.read_csv(filepath, comment="#")
        if "time" not in df.columns:
            # Fallback if there are comment lines without #
            df = pd.read_csv(filepath, skiprows=3)
        
        df["time"] = pd.to_datetime(df["time"])
        df = df.sort_values("time").reset_index(drop=True)
        return df

    def load_data(self) -> pd.DataFrame:
        if self._target_df is None:
            self._target_df = self._read_csv_file(self.target_file)
        return self._target_df

    def get_neighbor_data(self) -> Dict[str, pd.DataFrame]:
        if not self._neighbor_dfs:
            for st_id, info in self.neighbor_files.items():
                self._neighbor_dfs[st_id] = self._read_csv_file(info["path"])
        return self._neighbor_dfs

    def get_station_metadata(self) -> Dict[str, Dict]:
        meta = {"target": self.target_metadata, "neighbors": {}}
        for st_id, info in self.neighbor_files.items():
            meta["neighbors"][st_id] = {k: v for k, v in info.items() if k != "path"}
        return meta


class SyntheticNeighborSource(WeatherDataSource):
    """
    Stand-in data source for scaling network simulations to N arbitrary stations.
    Generates realistic correlated spatial neighbors by perturbing target station telemetry.
    """

    def __init__(self, target_csv_path: str = "open-meteo-30_25N74_25E189m.csv", num_neighbors: int = 5):
        self.target_csv_path = target_csv_path
        self.num_neighbors = num_neighbors
        self._target_df = None

    def load_data(self) -> pd.DataFrame:
        if self._target_df is None:
            df = pd.read_csv(self.target_csv_path, comment="#")
            df["time"] = pd.to_datetime(df["time"])
            self._target_df = df.sort_values("time").reset_index(drop=True)
        return self._target_df

    def get_neighbor_data(self) -> Dict[str, pd.DataFrame]:
        target = self.load_data()
        neighbors = {}
        np.random.seed(42)
        
        for i in range(1, self.num_neighbors + 1):
            st_id = f"SYNTHETIC_STATION_{i}"
            dist = i * 40.0 # km away
            noise_scale_temp = 0.5 + 0.1 * i
            noise_scale_rh = 2.0 + 0.5 * i
            noise_scale_press = 0.8 + 0.2 * i
            
            df_synth = target.copy()
            df_synth["temperature_2m"] += np.random.normal(0, noise_scale_temp, len(df_synth))
            df_synth["relative_humidity_2m"] = np.clip(
                df_synth["relative_humidity_2m"] + np.random.normal(0, noise_scale_rh, len(df_synth)), 0, 100
            )
            df_synth["surface_pressure"] += np.random.normal(0, noise_scale_press, len(df_synth))
            df_synth["pressure_msl"] += np.random.normal(0, noise_scale_press, len(df_synth))
            
            neighbors[st_id] = df_synth

        return neighbors

    def get_station_metadata(self) -> Dict[str, Dict]:
        return {
            "target": {"station_id": "TARGET", "lat": 30.25, "lon": 74.25, "elevation": 189, "distance_km": 0.0},
            "neighbors": {
                f"SYNTHETIC_STATION_{i}": {
                    "lat": 30.25 + i*0.1, "lon": 74.25 + i*0.1, "elevation": 189 + i*5, "distance_km": i*40.0, "corr_temp": max(0.80, 0.98 - i*0.03)
                } for i in range(1, self.num_neighbors + 1)
            }
        }


class OpenMeteoAPISource(WeatherDataSource):
    """
    Pluggable REST API source for pulling live or historical data from Open-Meteo API.
    Used for live deployment mode.
    """

    def __init__(self, lat: float = 30.25, lon: float = 74.25, elevation: int = 189):
        self.lat = lat
        self.lon = lon
        self.elevation = elevation

    def load_data(self) -> pd.DataFrame:
        import urllib.request
        import json
        url = (f"https://api.open-meteo.com/v1/forecast?latitude={self.lat}&longitude={self.lon}"
               f"&elevation={self.elevation}&hourly=temperature_2m,relative_humidity_2m,surface_pressure,pressure_msl")
        req = urllib.request.urlopen(url)
        data = json.loads(req.read().decode("utf-8"))
        df = pd.DataFrame(data["hourly"])
        df["time"] = pd.to_datetime(df["time"])
        return df

    def get_neighbor_data(self) -> Dict[str, pd.DataFrame]:
        # Implementation for pulling live neighbor stations via REST API
        return {}

    def get_station_metadata(self) -> Dict[str, Dict]:
        return {
            "target": {"station_id": "LIVE_API_STATION", "lat": self.lat, "lon": self.lon, "elevation": self.elevation, "distance_km": 0.0},
            "neighbors": {}
        }
