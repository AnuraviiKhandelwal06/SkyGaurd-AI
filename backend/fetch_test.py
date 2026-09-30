import os
import sys
import numpy as np
import pandas as pd
import requests

def fetch_historical_open_meteo(lat=28.61, lon=77.20, start_date='2023-01-01', end_date='2023-12-31'):
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m,relative_humidity_2m,surface_pressure,pressure_msl"
    print(f"Fetching from: {url}")
    r = requests.get(url)
    data = r.json()
    if 'hourly' not in data:
        raise ValueError(f"Failed to fetch data: {data}")
    
    hourly = data['hourly']
    df = pd.DataFrame({
        'time': hourly['time'],
        'temperature_2m': hourly['temperature_2m'],
        'relative_humidity_2m': hourly['relative_humidity_2m'],
        'surface_pressure': hourly['surface_pressure'],
        'pressure_msl': hourly['pressure_msl']
    })
    
    # Forward fill missing values
    df.ffill(inplace=True)
    df.bfill(inplace=True)
    
    df['station_id'] = 'AWS-REAL'
    df['is_anomaly'] = 0
    df['anomaly_type'] = 'CLEAN'
    return df

df = fetch_historical_open_meteo()
print(f"Fetched {len(df)} rows.")
print(df.head())
