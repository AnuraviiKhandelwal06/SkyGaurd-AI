import re

with open('src/pages/Livestations.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('<th className="p-4">Location</th>', '<th className="p-4">Station Name</th>\n              <th className="p-4">Location</th>')
content = content.replace('<td className="p-4">{station.location}</td>', '<td className="p-4">{station.station_name || "-"}</td>\n                <td className="p-4">{station.location}</td>')

with open('src/pages/Livestations.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
