import os
import sys
import logging

# We just want to print the final output
logging.basicConfig(level=logging.ERROR)
sys.path.append(os.path.join(os.getcwd(), 'backend'))

import app.services.ingestion_service as ig

print("--- LIVE POLL CYCLE ---")
ig.poll_stations()
