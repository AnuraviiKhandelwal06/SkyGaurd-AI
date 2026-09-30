with open('app/api/routes/predict.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('"AWS-001": (28.6139, 77.2090, "New Delhi", True)', '"AWS-001": (30.25, 74.25, "New Delhi", True)')
with open('app/api/routes/predict.py', 'w', encoding='utf-8') as f:
    f.write(content)
