import sys

path = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\backend\app\api\routes\predict.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_s = '"station_name": f"{station.location_name} AWS Node",'
new_s = '"station_name": station.location_name,'
if old_s in content:
    content = content.replace(old_s, new_s)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched predict.py")
else:
    print("Not found in predict.py")
