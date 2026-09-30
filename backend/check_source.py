import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from app.core.database import SessionLocal
from app.models.reading import Reading
from sqlalchemy import func

db = SessionLocal()
counts = db.query(Reading.source, func.count(Reading.id)).filter(Reading.station_id == 'AWS-001').group_by(Reading.source).all()
for source, count in counts:
    print(f"Source: {source.name if hasattr(source, 'name') else source}, Count: {count}")
