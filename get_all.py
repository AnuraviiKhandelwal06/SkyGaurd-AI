import requests
import json
r = requests.get('http://localhost:8000/predict/all')
print(json.dumps(r.json(), indent=2))
