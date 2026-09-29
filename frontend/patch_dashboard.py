import re

with open('src/pages/dashboard.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('<LiveReadings />', '<LiveReadings stationsData={stations} />')
content = content.replace('<RecentAlerts />', '<RecentAlerts stationsData={stations} />')

with open('src/pages/dashboard.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
