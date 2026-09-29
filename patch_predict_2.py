import sys

path = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\backend\app\api\routes\predict.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('sensor_temp += 15.2', 'sensor_temp += 4.5')
content = content.replace('sensor_temp -= 12.0', 'sensor_temp -= 4.5')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched predict.py properly")
