import sys

path = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\frontend\src\components\RecentAlerts.jsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_p = '''      <p className="text-xs text-gray-400 mt-6 pt-4 border-t border-gray-100">
        Demo station-status alerts, not verified anomaly events.
      </p>'''
if old_p in content:
    content = content.replace(old_p, '')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched RecentAlerts.jsx")
