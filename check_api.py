import requests
import json
r = requests.get('http://localhost:8000/predict?station_id=AWS-002')
print(json.dumps(r.json(), indent=2)[:1000])
