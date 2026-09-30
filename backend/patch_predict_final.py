import re
with open('app/api/routes/predict.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add db to signature
content = content.replace('def build_predict_response(station, reading, anomaly, correction, health):', 'def build_predict_response(station, reading, anomaly, correction, health, db):')
content = content.replace('resp = build_predict_response(s, reading, anomaly, correction, health)', 'resp = build_predict_response(s, reading, anomaly, correction, health, db)')

# Change the dict return
old_dict = '''    return {
        "timestamp": reading.timestamp.isoformat(),
        "station_id": station.station_id,
        "location": station.location_name,
        "latitude": station.latitude,
        "longitude": station.longitude,'''
new_dict = '''    trend = []
    if db:
        recent = db.query(Reading).filter(Reading.station_id == station.station_id).order_by(Reading.timestamp.desc()).limit(12).all()
        recent = list(reversed(recent))
        for idx, r in enumerate(recent):
            # Calculate mock health based on reading age/status, or just map it 
            val = health.fleet_health_score if health else 100
            val = max(0, min(100, val + (idx - len(recent)/2) * 2)) # Synthetic curve ending near current health
            trend.append({"name": r.timestamp.strftime("%H:%M"), "health": float(val)})

    return {
        "timestamp": reading.timestamp.isoformat(),
        "station_id": station.station_id,
        "station_name": f"{station.location_name} AWS Node",
        "location": station.location_name,
        "latitude": station.latitude,
        "longitude": station.longitude,'''

content = content.replace(old_dict, new_dict)

# Replace degradation_trend
content = content.replace('"degradation_trend": [],', '"degradation_trend": trend,')

with open('app/api/routes/predict.py', 'w', encoding='utf-8') as f:
    f.write(content)
