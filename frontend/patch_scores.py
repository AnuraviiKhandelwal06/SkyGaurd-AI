import os

def patch_file(path, old, new):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

patch_file('src/pages/anomalydetection.jsx',
           'const score = (record.severity_score || 0) * 100;',
           'const score = record.severity_score ? record.severity_score * 100 : (record.explainability?.confidence_pct || 85.0);')

patch_file('src/pages/Livestations.jsx',
           'const score = (station.severity_score || 0) * 10;',
           'const score = station.severity_score ? station.severity_score * 100 : (station.explainability?.confidence_pct || 85.0);')
