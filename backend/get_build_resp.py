with open('app/api/routes/predict.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_func = False
for line in lines:
    if 'def build_predict_response' in line:
        in_func = True
    elif in_func and line.startswith('@'):
        break
    if in_func:
        print(line, end='')
