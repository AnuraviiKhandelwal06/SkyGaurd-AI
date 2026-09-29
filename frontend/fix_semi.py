with open('src/components/Indiamap.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("navigate(`/stations?station=${station.station_id}`);", "navigate(`/stations?station=${station.station_id}`)")

with open('src/components/Indiamap.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
