import os

path = r'C:\Users\aj132\OneDrive\Desktop\Anvi SIH Project\skyguard\pipeline\fault_classifier.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_fallback = '''        if not self.is_fitted:
            # Rule fallback before training
            return "CLEAN", 0.9, {c: (0.9 if c == "CLEAN" else 0.01) for c in self.CLASSES}'''
            
good_fallback = '''        if not self.is_fitted:
            # Rule fallback before training
            rate_temp = feature_vector[0]
            flatline = feature_vector[3]
            missing = feature_vector[4]
            temp_spat_z = feature_vector[10]
            
            if missing == 1.0: return "COMM_FAILURE", 0.9, {}
            if flatline > 2: return "FROZEN", 0.9, {}
            if abs(rate_temp) > 5.0 and temp_spat_z > 3.0: return "SPIKE", 0.9, {}
            if temp_spat_z > 3.0: return "DRIFT", 0.7, {}
            
            return "UNKNOWN_FAULT", 0.5, {}'''

content = content.replace(bad_fallback, good_fallback)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
