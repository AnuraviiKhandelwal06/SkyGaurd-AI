import re
import os

def replace_in_file(filepath, pattern, replacement):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# dashboard.jsx
replace_in_file(
    'src/pages/dashboard.jsx',
    r'const healthyStations = stations\.filter\(\s*\(station\) => station\.status === "Healthy"\s*\)\.length;',
    'const healthyStations = stations.filter(station => normalizeStatus(station.status) === "Healthy").length;'
)
replace_in_file(
    'src/pages/dashboard.jsx',
    r'const warningStations = stations\.filter\(\s*\(station\) => station\.status === "Warning"\s*\)\.length;',
    'const warningStations = stations.filter(station => normalizeStatus(station.status) === "Warning").length;'
)
replace_in_file(
    'src/pages/dashboard.jsx',
    r'const faultyStations = stations\.filter\(\s*\(station\) => station\.status === "Faulty"\s*\)\.length;',
    'const faultyStations = stations.filter(station => normalizeStatus(station.status) === "Faulty").length;'
)

# RecentAlerts.jsx
replace_in_file(
    'src/components/RecentAlerts.jsx',
    r'\(s\) => s\.status === "Warning" \|\| s\.status === "Faulty" \|\| s\.status === "critical"',
    '(s) => normalizeStatus(s.status) === "Warning" || normalizeStatus(s.status) === "Faulty"'
)
with open('src/components/RecentAlerts.jsx', 'r', encoding='utf-8') as f:
    content = f.read()
if 'import { normalizeStatus }' not in content:
    content = content.replace('import { useNavigate } from "react-router-dom";', 'import { useNavigate } from "react-router-dom";\nimport { normalizeStatus } from "../utils/statusHelper";')
with open('src/components/RecentAlerts.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

# sensorhealth.jsx
replace_in_file(
    'src/pages/sensorhealth.jsx',
    r'sensor\.status === "Healthy"',
    'normalizeStatus(sensor.status) === "Healthy"'
)
replace_in_file(
    'src/pages/sensorhealth.jsx',
    r'sensor\.status === "Warning"',
    'normalizeStatus(sensor.status) === "Warning"'
)

# anomalydetection.jsx
replace_in_file(
    'src/pages/anomalydetection.jsx',
    r'record\.status === "resolved"',
    'normalizeStatus(record.status) === "Healthy"'
)
replace_in_file(
    'src/pages/anomalydetection.jsx',
    r'selected\.status === "resolved"',
    'normalizeStatus(selected.status) === "Healthy"'
)

print("Patched.")
