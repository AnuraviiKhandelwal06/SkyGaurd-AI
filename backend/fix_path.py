import re
with open('app/api/routes/predict.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('os.path.join(os.path.dirname(__file__), "../../../skyguard/models")', 'os.path.join(os.path.dirname(__file__), "../../../../skyguard/models")')
with open('app/api/routes/predict.py', 'w', encoding='utf-8') as f:
    f.write(content)
