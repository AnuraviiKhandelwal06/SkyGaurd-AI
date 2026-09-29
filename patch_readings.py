import sys

path = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\frontend\src\components\Livereadings.jsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_p = '''      <p className="text-xs text-gray-400 mt-6">
        Demo readings - not live IMD observations.
      </p>'''
if old_p in content:
    content = content.replace(old_p, '')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched Livereadings.jsx")
