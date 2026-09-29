import os

# Fix anomalydetection.jsx
with open('src/pages/anomalydetection.jsx', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('await fetch(/api/corrections//decision', 'await fetch(${BASE_URL}/api/corrections//decision')
with open('src/pages/anomalydetection.jsx', 'w', encoding='utf-8') as f:
    f.write(c)

# Fix sensorhealth.jsx
with open('src/pages/sensorhealth.jsx', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('const key = -;', 'const key = ${selectedId}-;')
c = c.replace('const key = -;', 'const key = ${selectedId}-;')  # if any
with open('src/pages/sensorhealth.jsx', 'w', encoding='utf-8') as f:
    f.write(c)

# Fix Livestations.jsx
with open('src/pages/Livestations.jsx', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('className={px-4 py-2 rounded-lg cursor-pointer }', 'className={px-4 py-2 rounded-lg cursor-pointer }')
with open('src/pages/Livestations.jsx', 'w', encoding='utf-8') as f:
    f.write(c)
