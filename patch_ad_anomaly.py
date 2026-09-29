import re

path = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\frontend\src\pages\anomalydetection.jsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the span that displays anomaly_type
pattern1 = r'<span[^>]*>\{record\.anomaly_type\s*\|\|\s*"UNKNOWN"\}</span>'
content = re.sub(pattern1, '', content, flags=re.IGNORECASE)

# 2. Remove the "Suspected fault" block if it's there
pattern2 = r'<p>\s*<strong>Suspected fault:</strong>\{"\s*"\}\s*\{selected\.anomaly_type\}\s*</p>'
content = re.sub(pattern2, '', content, flags=re.IGNORECASE)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Regex replace completed for anomalydetection.jsx.")
