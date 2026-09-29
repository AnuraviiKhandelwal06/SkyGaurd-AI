import sys

path = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\frontend\src\pages\settings.jsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_s = '<div className="mb-8">'
new_s = '<div className="mb-8 text-center">'
if old_s in content:
    content = content.replace(old_s, new_s)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched settings.jsx text-center")
else:
    print("Not found in settings.jsx")
