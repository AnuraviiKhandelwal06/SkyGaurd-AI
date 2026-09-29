import urllib.request
import json

def test_jump(jump):
    req = urllib.request.Request(f'http://localhost:8080/api/ingest/AWS-003?force_temp={30.0 + jump}', method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(f"Jump {jump}: {data['diagnosis']['diagnosis']['diagnosis_type']}")
    except Exception as e:
        print(f"Jump {jump} error: {e}")

for j in [1.0, 2.0, 2.5, 3.0, 5.0, 15.0]:
    test_jump(j)
