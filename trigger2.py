import urllib.request
import time

stations = ["AWS-001", "AWS-002", "AWS-003", "AWS-004", "AWS-005"]
for st in stations:
    req = urllib.request.Request(f'http://localhost:8080/api/ingest/{st}', method='POST')
    try:
        urllib.request.urlopen(req)
        print(f"Triggered {st}")
    except Exception as e:
        print(f"Error {st}: {e}")
    time.sleep(1)
