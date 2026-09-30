import re

file_path = 'app/services/ingestion_service.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('../../../data/College_station_Data.csv', '../../data/College_station_Data.csv')
content = content.replace('../../../data/csv_state.txt', '../../data/csv_state.txt')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
