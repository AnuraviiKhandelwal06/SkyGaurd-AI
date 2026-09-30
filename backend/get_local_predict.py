import os, sys, json
sys.path.append(os.getcwd())
from app.core.database import SessionLocal
from app.api.routes.predict import predict_all

db = SessionLocal()
results = predict_all(db)
# Just print AWS-001 result to verify trend and station_name
print(json.dumps(results[0], indent=2))
