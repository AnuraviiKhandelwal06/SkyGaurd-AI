import re

with open('src/components/Indiamap.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'console\.warn\(Station  missing coordinates\. Skipping map marker\.\);', r'console.warn(Station  missing coordinates. Skipping map marker.);', content)
content = re.sub(r'navigate\(/stations\?station=\)', r'navigate(/stations?station=)', content)

with open('src/components/Indiamap.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

