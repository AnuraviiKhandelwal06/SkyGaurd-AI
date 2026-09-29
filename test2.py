import urllib.request
import json
req = urllib.request.Request('http://localhost:8080/api/ingest/AWS-003?force_temp=31.0', method='POST')
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    print(json.dumps(data['diagnosis'], indent=2))
