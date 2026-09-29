from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append('backend')
from app.models.station import Station
from app.models.anomaly import Anomaly

engine = create_engine('sqlite:///backend/skyguard.db')
Session = sessionmaker(bind=engine)
db = Session()

anomalies = db.query(Anomaly).all()
for a in anomalies:
    print(f"ID: {a.id} | Station: {a.station_id} | Status: {a.status} | Fault Type: {a.fault_type}")
