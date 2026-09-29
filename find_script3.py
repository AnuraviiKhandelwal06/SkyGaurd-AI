import json

with open('C:/Users/aj132/.gemini/antigravity/brain/f9d5d373-102e-400a-8b64-1df93175ab19/.system_generated/logs/transcript_full.jsonl', 'r', encoding='utf-8') as f:
    content = f.read()
    idx = content.find("=== 3. RE-CALCULATE CLEANUP SET CORRECTLY ===")
    if idx != -1:
        script_idx = content.rfind("import sqlite3", 0, idx)
        print(content[script_idx:idx][:4000])

        # there must be a script that prints "TEST_ONLY: ... DUPLICATE_ONLY: ... OVERLAP: ..."
        script_idx2 = content.rfind("import sqlite3", 0, script_idx-10)
        print("------- ANOTHER SCRIPT -------")
        print(content[script_idx2:script_idx][:4000])

