import sqlite3
import pandas as pd

conn = sqlite3.connect('backend/skyguard.db')
readings = pd.read_sql_query("SELECT id, station_id FROM readings", conn)

dup_ids_not_in_142 = {256, 260, 287, 295, 299, 307, 311, 319, 323, 331, 335, 213, 217, 225, 236, 365, 367, 371, 244, 373, 248}

for d in dup_ids_not_in_142:
    st = readings[readings['id'] == d]['station_id'].iloc[0]
    if st != 'AWS-001':
        print("Wait, non AWS-001 found:", d, st)
print("If nothing printed above, all 21 are AWS-001.")
