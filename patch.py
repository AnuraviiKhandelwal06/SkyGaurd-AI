lines = open('backend/app/api/routes/predict.py').read().split('\n')
for i, line in enumerate(lines):
    if 'from app.models.station import Station' in line:
        lines[i] = 'from app.models.station import Station, StationStatus'
        break
with open('backend/app/api/routes/predict.py', 'w') as f:
    f.write('\n'.join(lines))
