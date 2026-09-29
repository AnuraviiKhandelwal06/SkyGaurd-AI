import json
import re

with open('C:/Users/aj132/.gemini/antigravity/brain/f9d5d373-102e-400a-8b64-1df93175ab19/.system_generated/logs/transcript_full.jsonl', 'r', encoding='utf-8') as f:
    content = f.read()
    
    # find all lists of integers
    lists = re.findall(r'\[([0-9\s,]+)\]', content)
    for lst in lists:
        nums = [n.strip() for n in lst.split(',') if n.strip().isdigit()]
        if len(nums) == 142:
            print("FOUND 142 IDs!")
            print(nums)
            
    # Also find any block saying "TEST_ONLY"
    blocks = re.findall(r'.{0,200}TEST_ONLY.{0,500}', content, re.DOTALL)
    for i, b in enumerate(blocks[:3]):
        print(f"--- BLOCK {i} ---")
        print(b.replace('\n', ' '))

