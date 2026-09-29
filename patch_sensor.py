import re

path = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\frontend\src\pages\sensorhealth.jsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'<p[^>]*>[\s\r\n]*Demonstration data[^<]*not live sensor diagnostics\.[\s\r\n]*</p>'
content = re.sub(pattern, '', content, flags=re.IGNORECASE)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Regex replace completed for sensorhealth.jsx.")
