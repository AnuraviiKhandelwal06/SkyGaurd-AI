import urllib.request
import json
import time
time.sleep(2)
req = urllib.request.urlopen("http://localhost:8080/predict/all")
data = json.loads(req.read())
for d in data:
    trend = d.get("sensor_health", {}).get("degradation_trend", [])
    print(d["station_name"], [t.get("health") for t in trend])
