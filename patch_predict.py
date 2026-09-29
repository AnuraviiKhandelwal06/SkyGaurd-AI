import os

path = 'C:/Users/aj132/OneDrive/Desktop/Anvi SIH Project/backend/app/api/routes/predict.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_code = '''    # Generate realistic reading with synthetic fault injection
    base_temp = 30.0
    if force_temp is not None:
        base_temp = force_temp
    else:
        if station_id == "AWS-002":
            base_temp = 34.2 # Drift
        elif station_id == "AWS-004":
            base_temp = 62.1 # Spike
        elif station_id == "AWS-003":
            base_temp = 12.0 # Genuine Event

    t = base_temp + random.uniform(-0.5, 0.5)
    rh = random.uniform(40, 80)
    p = random.uniform(990, 1010)

    reading = Reading(
        station_id=station_id,
        timestamp=datetime.now(timezone.utc),
        temperature=t,
        humidity=rh,
        pressure=p,
        source=ReadingSource.physical_sensor
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)

    reading_dict = {
        "time": reading.timestamp.isoformat(),
        "temperature_2m": reading.temperature,
        "relative_humidity_2m": reading.humidity,
        "surface_pressure": reading.pressure,
        "pressure_msl": reading.pressure + 20, # required field
        "station_id": station_id
    }

    # Run ML Pipeline
    pl = get_pipeline()
    # Add neighbors so spatial isolation works
    nt = neighbor_temp if neighbor_temp is not None else 30.0
    neighbors = {
        "AWS-1": {"temperature_2m": nt, "relative_humidity_2m": 50, "surface_pressure": 1000, "pressure_msl": 1020},
        "AWS-2": {"temperature_2m": nt + 0.5, "relative_humidity_2m": 48, "surface_pressure": 1001, "pressure_msl": 1021},
    }'''

new_code = '''    # Step 1: Fetch REAL ground truth data from Open-Meteo for comparison
    try:
        real_data = fetch_weather_api(station.latitude, station.longitude)
        real_temp = real_data.get("temperature", 30.0)
        real_humidity = real_data.get("humidity", 50.0)
        real_pressure = real_data.get("pressure", 1000.0)
    except Exception as e:
        # Fallback if API fails
        real_temp = 30.0
        real_humidity = 50.0
        real_pressure = 1000.0

    # Step 2: "Hum denge" - User provided sensor data (or mock sensor faults)
    # We apply the faults over the REAL meteo data to simulate the faulty sensor
    if force_temp is not None:
        sensor_temp = force_temp
    else:
        sensor_temp = real_temp
        if station_id == "AWS-002":
            sensor_temp += 15.2 # Drift fault
        elif station_id == "AWS-004":
            sensor_temp += 35.0 # Massive Spike fault
        elif station_id == "AWS-003":
            # Genuine Event (Weather naturally changed, maybe we just fake the sensor seeing a legit drop, 
            # but then Open Meteo should technically also show it. For testing, we mock both, 
            # or we simulate the sensor reading dropping)
            sensor_temp -= 12.0
            
    # Add minor sensor noise
    sensor_temp += random.uniform(-0.5, 0.5)

    reading = Reading(
        station_id=station_id,
        timestamp=datetime.now(timezone.utc),
        temperature=sensor_temp,
        humidity=real_humidity + random.uniform(-2, 2),
        pressure=real_pressure + random.uniform(-1, 1),
        source=ReadingSource.physical_sensor
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)

    reading_dict = {
        "time": reading.timestamp.isoformat(),
        "temperature_2m": reading.temperature,
        "relative_humidity_2m": reading.humidity,
        "surface_pressure": reading.pressure,
        "pressure_msl": reading.pressure + 20, 
        "station_id": station_id
    }

    # Run ML Pipeline
    pl = get_pipeline()
    
    # Step 3: Compare sensor data against the REAL Open-Meteo data as the "Neighbor" baseline
    neighbors = {
        "OpenMeteo-Truth": {
            "temperature_2m": real_temp, 
            "relative_humidity_2m": real_humidity, 
            "surface_pressure": real_pressure, 
            "pressure_msl": real_pressure + 20
        }
    }'''

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched predict.py successfully!")
else:
    print("Could not find old_code string in predict.py!")
