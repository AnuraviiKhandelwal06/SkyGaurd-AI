with open('app/services/ingestion_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('from app.models.health import SensorHealth', 'from app.models.sensor_health import SensorHealth')
content = content.replace('from app.models.history import FaultHistory', 'from app.models.fault_history import FaultHistory')

with open('app/services/ingestion_service.py', 'w', encoding='utf-8') as f:
    f.write(content)
