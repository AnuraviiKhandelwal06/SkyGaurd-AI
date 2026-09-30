import sys
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("Ingesting data for stations...")
for _ in range(3):
    for st in ['AWS-001', 'AWS-002', 'AWS-003', 'AWS-004']:
        response = client.post(f"/api/ingest/{st}")
        if response.status_code != 200:
            print(f"Error {st}:", response.json())
        else:
            print(f"Success {st}: status {response.json().get('diagnosis', {}).get('status')}")

print("\nRunning test_pipeline_flow.py...")
import subprocess
subprocess.run([sys.executable, '../test_pipeline_flow.py'], cwd='..')

