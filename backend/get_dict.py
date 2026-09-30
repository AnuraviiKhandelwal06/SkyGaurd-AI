with open('app/api/routes/predict.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
start = content.find('return {')
end = content.find('    }', start) + 5
print(content[start:end])
