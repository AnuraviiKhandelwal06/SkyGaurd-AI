import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.services.ingestion_service import poll_stations

print("Running poll_stations()...")
poll_stations()
print("Done polling.")
