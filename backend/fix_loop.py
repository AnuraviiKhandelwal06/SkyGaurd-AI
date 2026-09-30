with open('app/services/ingestion_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = '''        for station in stations:
            reading_data = None
            if station.is_primary:
                try:
                    data = fetch_primary_sensor()
                    reading_data = {
                        "temperature": data.get("temperature"),
                        "humidity": data.get("humidity"),
                        "pressure": data.get("pressure")
                    }
                except Exception as e:
                    logger.error(f"Error polling primary station {station.station_id}: {e}")
                    continue
            else:
                try:
                    reading_data = fetch_weather_api(station.latitude, station.longitude)
                except Exception as e:
                    logger.error(f"Error fetching Open-Meteo for {station.station_id}: {e}")
                    continue
            
            try:
                if reading_data.get("temperature") is None:
                    raise ValueError("Sensor returned no temperature")'''

import re
# We need to replace the loop logic
content = re.sub(r'        for station in stations:\n            if not station\.is_primary:\n                continue # Only poll primary sensor in this hardware integration\n                \n            try:\n                data = fetch_primary_sensor\(\)\n                reading_data = \{\n                    "temperature": data\.get\("temperature"\),\n                    "humidity": data\.get\("humidity"\),\n                    "pressure": data\.get\("pressure"\)\n                \}\n                \n                if reading_data\["temperature"\] is None:\n                    raise ValueError\("Sensor returned no temperature"\)', replacement, content)

with open('app/services/ingestion_service.py', 'w', encoding='utf-8') as f:
    f.write(content)
