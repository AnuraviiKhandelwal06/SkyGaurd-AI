import os
import json
import datetime

history_dir = os.path.expandvars('%APPDATA%\\Code\\User\\History')
target_time_start = datetime.datetime.fromisoformat('2026-09-27T10:00:00')
target_time_end = datetime.datetime.fromisoformat('2026-09-27T14:00:00')

results = []
if os.path.exists(history_dir):
    for d in os.listdir(history_dir):
        dp = os.path.join(history_dir, d)
        if os.path.isdir(dp):
            entries_file = os.path.join(dp, 'entries.json')
            if os.path.exists(entries_file):
                try:
                    with open(entries_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    resource = data.get('resource', '')
                    if 'frontend/src' in resource.replace('\\\\', '/'):
                        for entry in data.get('entries', []):
                            timestamp_ms = entry.get('timestamp', 0)
                            dt = datetime.datetime.fromtimestamp(timestamp_ms / 1000.0)
                            if target_time_start <= dt <= target_time_end:
                                results.append(f"{resource} @ {dt}")
                except:
                    pass

for r in results:
    print(r)
