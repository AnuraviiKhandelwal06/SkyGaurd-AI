import requests
import json
res = requests.get('http://localhost:8080/predict/all')
print(json.dumps(res.json(), indent=2))
