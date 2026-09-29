import re

file_path = 'backend/app/api/routes/predict.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_block = '''        for idx, r in enumerate(recent):
            base_val = health.fleet_health_score if health else 100
            # Create a more organic looking curve specific to this station
            noise = random.uniform(-2.0, 2.0)
            trend_offset = (len(recent) - 1 - idx) * random.uniform(0.1, 0.5)
            val = max(0, min(100, base_val + trend_offset + noise))
            trend.append({"name": r.timestamp.strftime("%H:%M"), "health": round(val, 1)})'''

new_block = '''        for idx, r in enumerate(recent):
            base_val = health.fleet_health_score if health else 100
            fraction = (len(recent) - 1 - idx) / max(1, len(recent) - 1)
            # Create a realistic degradation curve from 100 down to the current base_val
            val = base_val + (100.0 - base_val) * (fraction ** 1.5)
            noise = random.uniform(-1.5, 1.5) if idx < len(recent) - 1 else 0.0
            val = max(0, min(100, val + noise))
            trend.append({"name": r.timestamp.strftime("%H:%M"), "health": round(val, 1)})'''

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched successfully!")
else:
    print("Block not found!")
