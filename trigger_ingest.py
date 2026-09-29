import requests

stations = ["AWS-001", "AWS-002", "AWS-003", "AWS-004", "AWS-005"]
for st in stations:
    r = requests.post(f'http://localhost:8000/api/ingest/{st}')
    print(r.status_code, r.text[:50])
