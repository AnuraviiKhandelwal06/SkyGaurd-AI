import re

with open('src/components/Indiamap.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("Temperature: {station.original_telemetry.temperature_2m?.toFixed(1)} C", "Temperature: {station.original_telemetry.temperature_2m?.toFixed(1)} \u00B0C")

with open('src/components/Indiamap.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
