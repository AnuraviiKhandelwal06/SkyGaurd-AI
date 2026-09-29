import re

path = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\frontend\src\pages\Livestations.jsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the exact paragraph using regex
pattern = r'<p[^>]*>[\s\r\n]*Demonstration data[^<]*not live IMD observations\.[\s\r\n]*</p>'
content = re.sub(pattern, '', content, flags=re.IGNORECASE)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Regex replace completed for Livestations.jsx.")
