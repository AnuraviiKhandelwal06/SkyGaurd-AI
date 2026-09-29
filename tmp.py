import urllib.request
import json
req = urllib.request.urlopen("http://localhost:8080/predict/all")
data = json.loads(req.read())
for d in data:
    print(d["station_name"], d.get("severity_score"), d.get("diagnosis", {}).get("diagnosis_type"))
