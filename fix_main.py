import sys

path = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\skyguard\main_pipeline.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace any remaining fault_label with fault_type
content = content.replace('fault_label', 'fault_type')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
