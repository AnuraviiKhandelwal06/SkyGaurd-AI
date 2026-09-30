import os
import sys
import numpy as np
import pandas as pd
import requests
import time

sys.path.append(os.getcwd())
from skyguard.main_pipeline import SkyGuardPipeline
from skyguard.data.injector import SyntheticAnomalyInjector

def fetch_historical_open_meteo_chunked(lat=28.61, lon=77.20, start_date='2023-01-01', end_date='2023-12-31'):
    print("Fetching Open-Meteo data in chunks to prevent timeout...")
    df_list = []
    current_start = pd.to_datetime(start_date)
    final_end = pd.to_datetime(end_date)
    
    while current_start <= final_end:
        current_end = current_start + pd.DateOffset(months=3)
        if current_end > final_end:
            current_end = final_end
            
        s_date = current_start.strftime('%Y-%m-%d')
        e_date = current_end.strftime('%Y-%m-%d')
        url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={s_date}&end_date={e_date}&hourly=temperature_2m,relative_humidity_2m,surface_pressure,pressure_msl"
        print(f"Fetching chunk {s_date} to {e_date}...")
        
        try:
            r = requests.get(url, timeout=30)
            data = r.json()
            if 'hourly' not in data:
                print(f"Failed to fetch chunk: {data}")
            else:
                hourly = data['hourly']
                chunk_df = pd.DataFrame({
                    'time': hourly['time'],
                    'temperature_2m': hourly['temperature_2m'],
                    'relative_humidity_2m': hourly['relative_humidity_2m'],
                    'surface_pressure': hourly['surface_pressure'],
                    'pressure_msl': hourly['pressure_msl']
                })
                # Convert all numeric columns to float to avoid LossySetitemError
                for col in ['temperature_2m', 'relative_humidity_2m', 'surface_pressure', 'pressure_msl']:
                    chunk_df[col] = chunk_df[col].astype(float)
                df_list.append(chunk_df)
        except Exception as e:
            print(f"Error fetching chunk: {e}")
            
        current_start = current_end + pd.DateOffset(days=1)
        time.sleep(1) # rate limit
        
    if not df_list:
        print("Fallback to generated data...")
        from app.api.routes.predict import generate_dummy_training_data
        return generate_dummy_training_data(8760)

    df = pd.concat(df_list, ignore_index=True)
    df.ffill(inplace=True)
    df.bfill(inplace=True)
    df['station_id'] = 'AWS-REAL'
    df['is_anomaly'] = 0
    df['anomaly_type'] = 'CLEAN'
    return df

print("Fetching Open-Meteo 1-year real history...")
clean_df = fetch_historical_open_meteo_chunked()
print(f"Fetched {len(clean_df)} hours of real data.")

print("Injecting anomalies (multiple seeds & magnitudes)...")
all_corrupted = []
for seed in [42, 99, 123]:
    injector = SyntheticAnomalyInjector(seed=seed)
    corrupted_df = injector.inject_anomalies(clean_df.copy())
    all_corrupted.append(corrupted_df)

merged_corrupted = pd.concat(all_corrupted, ignore_index=True)

clean_indices = merged_corrupted[merged_corrupted["is_anomaly"] == 0].index.tolist()
valid_clean = [i for i in clean_indices if i >= 24]
np.random.seed(999)
genuine_idx = np.random.choice(valid_clean, 300, replace=False)
for idx in genuine_idx:
    merged_corrupted.loc[idx, "anomaly_type"] = "GENUINE_EXTREME"
    merged_corrupted.loc[idx, "is_anomaly"] = 1
    merged_corrupted.loc[idx, "temperature_2m"] += np.random.uniform(10, 20) * np.random.choice([-1, 1])

print(f"Training pipeline models on {len(clean_df)} clean rows and {len(merged_corrupted)} corrupted rows...")
pipeline = SkyGuardPipeline()
pipeline.fit(train_df=clean_df, synthetic_corrupted_val_df=merged_corrupted)

model_dir = os.path.join(os.path.dirname(__file__), "../skyguard/models")
os.makedirs(model_dir, exist_ok=True)
pipeline.fault_classifier.save(os.path.join(model_dir, "classifier.pkl"))
pipeline.temporal_ai.save(os.path.join(model_dir, "temporal"))
print("Models saved successfully!")
