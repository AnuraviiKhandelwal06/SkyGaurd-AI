import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

os.makedirs('backend/data', exist_ok=True)
csv_file = 'backend/data/College_station_Data.csv'

# Generate 155 rows
num_rows = 155
start_time = datetime(2026, 9, 29, 12, 0, 0)

timestamps = [start_time + timedelta(minutes=5*i) for i in range(num_rows)]
raw_timestamps = [int(t.timestamp()) for t in timestamps]

# Realistic DHT22 data (temp around 25-30, humidity 40-60)
# Add some smooth variations
np.random.seed(42)
temp = 28.0 + np.cumsum(np.random.normal(0, 0.2, num_rows))
humidity = 50.0 + np.cumsum(np.random.normal(0, 0.5, num_rows))
# Simulated pressure around 1010
pressure = 1010.0 + np.cumsum(np.random.normal(0, 0.3, num_rows))

df = pd.DataFrame({
    'Timestamp': [t.strftime('%Y-%m-%d %H:%M:%S') for t in timestamps],
    'Raw_Timestamp': raw_timestamps,
    'Temperature_C': np.round(temp, 2),
    'Humidity': np.round(humidity, 2),
    'Pressure_Hpa': np.round(pressure, 2)
})
df.to_csv(csv_file, index=False)
print("CSV generated at", csv_file)
