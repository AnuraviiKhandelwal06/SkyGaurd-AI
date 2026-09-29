from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append('backend')
from app.models.station import Station, StationStatus

engine = create_engine('sqlite:///backend/skyguard.db')
Session = sessionmaker(bind=engine)
db = Session()

st = db.query(Station).filter(Station.station_id == 'AWS-002').first()
print('Before:', st.status)
st.status = StationStatus.faulty
db.commit()
db.refresh(st)
print('After:', st.status)
