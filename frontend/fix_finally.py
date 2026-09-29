import re

with open('src/components/Indiamap.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("console.warn(Station  missing coordinates. Skipping map marker.);", "console.warn(`Station ${station.station_id} missing coordinates. Skipping map marker.`);")
content = content.replace("navigate(/stations?station=)", "navigate(`/stations?station=${station.station_id}`);")

with open('src/components/Indiamap.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
