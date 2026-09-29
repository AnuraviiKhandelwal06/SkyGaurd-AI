import sys

path = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\frontend\src\pages\Livestations.jsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove "Demonstration data - not live IMD observations."
old_p = '''      <p className="text-xs text-gray-400 mt-1 mb-6">
        Demonstration data - not live IMD observations.
      </p>'''
if old_p in content:
    content = content.replace(old_p, '')

old_p2 = '''      <p className="text-xs text-gray-400 mt-1 mb-6">
        Demonstration data ?" not live IMD observations.
      </p>'''
if old_p2 in content:
    content = content.replace(old_p2, '')

# 2. Remove the anomaly type span
old_span = '{station.anomaly_type && station.anomaly_type !== "CLEAN" && <span className="ml-2 text-xs text-gray-500">{station.anomaly_type}</span>}'
if old_span in content:
    content = content.replace(old_span, '')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched Livestations.jsx")
