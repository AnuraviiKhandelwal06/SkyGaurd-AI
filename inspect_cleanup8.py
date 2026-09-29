import sqlite3
import pandas as pd

conn = sqlite3.connect('backend/skyguard.db')
readings = pd.read_sql_query("SELECT * FROM readings WHERE id IN (357, 358)", conn)
print(readings[['id', 'timestamp', 'source']])
