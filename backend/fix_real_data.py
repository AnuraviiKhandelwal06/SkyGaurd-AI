import re

file_path = 'app/services/ingestion_service.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_block = '''            if station.is_primary:
                try:
                    data = fetch_csv_row()
                    reading_data = {
                        "temperature": data.get("temperature"),
                        "humidity": data.get("humidity"),
                        "pressure": data.get("pressure")
                    }
                except Exception as e:'''

new_block = '''            if station.is_primary:
                try:
                    real_data = fetch_weather_api(station.latitude, station.longitude)
                    data = fetch_csv_row()
                    reading_data = {
                        "temperature": data.get("temperature"),
                        "humidity": data.get("humidity"),
                        "pressure": data.get("pressure")
                    }
                except Exception as e:'''

content = content.replace(old_block, new_block)
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
