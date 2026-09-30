import urllib.request
import json
req = urllib.request.urlopen("http://localhost:8080/predict/all")
data = json.loads(req.read())
for d in data:
    if d['station_id'] == 'AWS-002':
        print(json.dumps(d, indent=2))
