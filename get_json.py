import requests
import json
r = requests.post('http://localhost:8000/api/ingest/AWS-004')
print(json.dumps(r.json(), indent=2))
