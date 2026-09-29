import sys

path = 'C:/Users/aj132/OneDrive\Desktop/Anvi SIH Project/backend/app/services/ingestion_service.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the part that fetches reading_data and handles neighbors
old_logic = '''                try:
                    reading_data = fetch_weather_api(station.latitude, station.longitude)
                except Exception as e:
                    logger.error(f"Error fetching Open-Meteo for {station.station_id}: {e}")
                    continue
            
            try:
                # -------------------------------------------------------------
                # INJECT SYNTHETIC ANOMALIES/WARNINGS AS DEFINED EARLIER
                # This ensures the dashboard sees Warning/Faulty/Anomalies
                # -------------------------------------------------------------
                import random
                if reading_data and station.station_id == "AWS-002":
                    # Drift Fault -> Faulty
                    reading_data["temperature"] += 15.2
                elif reading_data and station.station_id == "AWS-003":
                    # Genuine Event -> Warning
                    reading_data["temperature"] += 12.0
                elif reading_data and station.station_id == "AWS-004":
                    # Spike Fault -> Faulty
                    if random.random() < 0.5:
                        reading_data["temperature"] += 35.0
                
                if reading_data.get("temperature") is None:'''

new_logic = '''                try:
                    # FETCH REAL METEO DATA (Ground Truth)
                    real_data = fetch_weather_api(station.latitude, station.longitude)
                    
                    # Simulated Sensor Data 
                    # (User provides primary sensor data, or we mock the other AWS stations with faults)
                    reading_data = {
                        "time": real_data.get("time"),
                        "temperature": real_data.get("temperature", 30.0),
                        "humidity": real_data.get("humidity", 50.0),
                        "pressure": real_data.get("pressure", 1000.0)
                    }
                    
                    import random
                    if station.station_id == "AWS-002":
                        # Drift Fault -> Faulty
                        reading_data["temperature"] += 15.2
                    elif station.station_id == "AWS-003":
                        # Genuine Event -> Warning (simulate sensor dropping)
                        reading_data["temperature"] -= 12.0
                    elif station.station_id == "AWS-004":
                        # Spike Fault -> Faulty
                        if random.random() < 0.5:
                            reading_data["temperature"] += 35.0
                            
                except Exception as e:
                    logger.error(f"Error fetching Open-Meteo for {station.station_id}: {e}")
                    continue
            
            try:
                if reading_data.get("temperature") is None:'''

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    print("Patched part 1!")

old_neighbors = '''                # Compute valid spatial neighbors (<150km)
                neighbors = {}
                neighbor_meta = {}
                for n_st in stations:
                    if n_st.station_id == station.station_id:
                        continue
                    if n_st.latitude is None or n_st.longitude is None:
                        continue
                        
                    dist = haversine(station.latitude, station.longitude, n_st.latitude, n_st.longitude)
                    if dist <= 150.0:
                        # Get latest reading for this neighbor
                        n_read = db.query(Reading).filter(
                            Reading.station_id == n_st.station_id
                        ).order_by(Reading.timestamp.desc()).first()
                        
                        if n_read:
                            neighbors[n_st.station_id] = {
                                "temperature_2m": n_read.temperature,
                                "relative_humidity_2m": n_read.humidity,
                                "surface_pressure": n_read.pressure,
                                "pressure_msl": n_read.pressure + 20
                            }
                            neighbor_meta[n_st.station_id] = {
                                "distance_km": dist,
                                "corr_temp": 0.95
                            }
                
                pipeline.neighbor_metadata = neighbor_meta'''

new_neighbors = '''                # Compare Sensor Data against REAL Open-Meteo Data (as ground truth baseline)
                neighbors = {
                    "OpenMeteo-Truth": {
                        "temperature_2m": real_data.get("temperature", 30.0),
                        "relative_humidity_2m": real_data.get("humidity", 50.0),
                        "surface_pressure": real_data.get("pressure", 1000.0),
                        "pressure_msl": real_data.get("pressure", 1000.0) + 20
                    }
                }
                pipeline.neighbor_metadata = {
                    "OpenMeteo-Truth": {
                        "distance_km": 0.0,
                        "corr_temp": 1.0
                    }
                }'''

if old_neighbors in content:
    content = content.replace(old_neighbors, new_neighbors)
    print("Patched part 2!")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done patching ingestion_service.py")
