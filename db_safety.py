import os
import shutil
import sqlite3

source_db = 'backend/skyguard.db'
test_db = 'backend/skyguard_test.db'

# Make fresh copy
if os.path.exists(test_db):
    os.remove(test_db)
shutil.copy2(source_db, test_db)

source_size = os.path.getsize(source_db)
test_size = os.path.getsize(test_db)

def get_db_stats(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(id), COUNT(*) FROM readings')
    max_id, count = cursor.fetchone()
    conn.close()
    return max_id, count

s_max, s_count = get_db_stats(source_db)
t_max, t_count = get_db_stats(test_db)

print(f"Source DB path: {source_db}")
print(f"Test DB path: {test_db}")
print(f"Source DB file size: {source_size} bytes")
print(f"Test DB file size: {test_size} bytes")
print(f"Source DB max reading ID: {s_max}")
print(f"Source DB reading count: {s_count}")
print(f"Test DB max reading ID: {t_max}")
print(f"Test DB reading count: {t_count}")

