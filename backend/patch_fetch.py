with open('app/services/ingestion_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

fetch_func = '''def fetch_weather_api(lat: float, lon: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,surface_pressure"
    response = httpx.get(url, timeout=10.0)
    response.raise_for_status()
    data = response.json()
    current = data.get("current", {})
    return {
        "temperature": current.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "pressure": current.get("surface_pressure"),
    }

def fetch_primary_sensor():'''

content = content.replace('def fetch_primary_sensor():', fetch_func)

with open('app/services/ingestion_service.py', 'w', encoding='utf-8') as f:
    f.write(content)
