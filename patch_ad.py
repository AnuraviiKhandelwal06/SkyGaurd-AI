import sys

path = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\frontend\src\pages\anomalydetection.jsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Try to find the block
old_block = '''        <p className="text-gray-500 mt-1">
          Demonstration mode: anomaly results and corrections
          are sample data, not live AI predictions.
        </p>'''
if old_block in content:
    content = content.replace(old_block, '')
else:
    print("Could not find exact block, doing loose replace")
    content = content.replace('Demonstration mode: anomaly results and corrections\n          are sample data, not live AI predictions.', '')
    content = content.replace('Demonstration mode: anomaly results and corrections\r\n          are sample data, not live AI predictions.', '')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched anomalydetection.jsx")
