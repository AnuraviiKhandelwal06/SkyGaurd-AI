lines = open('skyguard/data/injector.py').read().split('\n')
for i, line in enumerate(lines):
    if 'corrupted_df.loc[idx, var] += magnitude' in line:
        lines[i] = '            corrupted_df.loc[idx, var] = float(corrupted_df.loc[idx, var]) + magnitude'
        break
with open('skyguard/data/injector.py', 'w') as f:
    f.write('\n'.join(lines))
