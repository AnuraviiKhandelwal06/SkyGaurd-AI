import json
import re

with open('C:/Users/aj132/.gemini/antigravity/brain/f9d5d373-102e-400a-8b64-1df93175ab19/.system_generated/logs/transcript_full.jsonl', 'r', encoding='utf-8') as f:
    content = f.read()
    
    # We found the block "=== 3. RE-CALCULATE CLEANUP SET CORRECTLY ==="
    idx = content.find("=== 3. RE-CALCULATE CLEANUP SET CORRECTLY ===")
    if idx != -1:
        # Search backwards for the python script that generated it
        script_idx = content.rfind("import sqlite3", 0, idx)
        if script_idx != -1:
            print("--- SCRIPT ---")
            print(content[script_idx:idx][:2000]) # print first 2000 chars of script

