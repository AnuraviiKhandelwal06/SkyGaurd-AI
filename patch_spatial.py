import sys

path = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\skyguard\pipeline\physics_spatial.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('std_temp = max(float(np.std(n_temps)), 0.5)', 'std_temp = max(float(np.std(n_temps)), 3.5)')
content = content.replace('std_rh = max(float(np.std(n_rhs)), 2.0)', 'std_rh = max(float(np.std(n_rhs)), 10.0)')
content = content.replace('std_sp = max(float(np.std(n_sps)), 1.0)', 'std_sp = max(float(np.std(n_sps)), 5.0)')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched physics_spatial.py")
