import re

with open('src/components/Indiamap.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('console.warn(Station  missing coordinates', 'console.warn(Station  missing coordinates')
content = content.replace('navigate(/stations?station=)', 'navigate(/stations?station=)')

with open('src/components/Indiamap.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
