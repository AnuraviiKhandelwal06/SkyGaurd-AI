import urllib.request
import json
for st in ['AWS-001', 'AWS-002', 'AWS-003', 'AWS-004', 'AWS-005']:
    req = urllib.request.Request(f'http://localhost:8080/api/ingest/{st}', method='POST')
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(st, data['diagnosis']['diagnosis']['diagnosis_type'], data['diagnosis'].get('anomaly_type'))
    except Exception as e:
        print(st, e)
