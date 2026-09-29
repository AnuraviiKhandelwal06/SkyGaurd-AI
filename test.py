import urllib.request
import json

req = urllib.request.urlopen("http://localhost:8080/predict/all")
data = json.loads(req.read())
print(json.dumps(data[0], indent=2))
