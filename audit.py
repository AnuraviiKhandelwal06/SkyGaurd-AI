import sqlite3
import os

db_path = 'backend/skyguard.db'
backup_path = 'backend/skyguard_backup_cleanup.db'

authorized_ids = {38, 39, 48, 49, 53, 54, 76, 77, 78, 79, 80, 81, 85, 86, 87, 99, 100, 101, 102, 107, 108, 109, 110, 111, 112, 113, 114, 119, 120, 121, 122, 123, 124, 125, 126, 194, 214, 215, 216, 218, 219, 220, 226, 227, 228, 237, 238, 239, 245, 246, 247, 249, 250, 251, 257, 258, 259, 261, 262, 263, 268, 269, 270, 271, 272, 273, 280, 281, 282, 284, 285, 286, 288, 289, 290, 296, 297, 298, 300, 301, 302, 308, 309, 310, 312, 313, 314, 320, 321, 322, 324, 325, 326, 332, 333, 334, 336, 337, 338, 339, 340, 341, 343, 344, 345, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 366, 368, 372, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390}

print('=== 2. PRODUCTION DB STATE ===')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
r_count = cur.execute('SELECT COUNT(*) FROM readings').fetchone()[0]
r_max = cur.execute('SELECT MAX(id) FROM readings').fetchone()[0]
a_count = cur.execute('SELECT COUNT(*) FROM anomalies').fetchone()[0]
c_count = cur.execute('SELECT COUNT(*) FROM corrections').fetchone()[0]
print(f'Reading_count = {r_count}')
print(f'Reading_max = {r_max}')
print(f'Anomaly_count = {a_count}')
print(f'Correction_count = {c_count}')

print('\n=== 3. 142 DELETION IDs ===')
placeholders = ','.join('?' for _ in authorized_ids)
cur.execute(f'SELECT COUNT(*) FROM readings WHERE id IN ({placeholders})', tuple(authorized_ids))
present_auth_ids = cur.fetchone()[0]
print(f'Present authorized deletion IDs = {present_auth_ids}')
if present_auth_ids > 0:
    cur.execute(f'SELECT id FROM readings WHERE id IN ({placeholders})', tuple(authorized_ids))
    print('Still present IDs:', [row[0] for row in cur.fetchall()])
print(f'Number of absent authorized IDs = {len(authorized_ids) - present_auth_ids}')

print('\n=== 4. UNAUTHORIZED DELETIONS ===')
conn_bak = sqlite3.connect(backup_path)
cur_bak = conn_bak.cursor()

cur_bak.execute('SELECT id FROM readings')
bak_ids = set(row[0] for row in cur_bak.fetchall())

cur.execute('SELECT id FROM readings')
curr_ids = set(row[0] for row in cur.fetchall())

diff_ids = bak_ids - curr_ids
print(f'pre-cleanup IDs - current IDs = authorized 142 IDs: {diff_ids == authorized_ids}')
unauthorized = diff_ids - authorized_ids
print(f'unauthorized Reading deletions = {len(unauthorized)}')
if unauthorized:
    print(f'Unauthorized IDs deleted: {unauthorized}')

print('\n=== 5. AWS-001 PROTECTION ===')
cur_bak.execute("SELECT id FROM readings WHERE station_id = 'AWS-001' ORDER BY id")
bak_aws1 = set(row[0] for row in cur_bak.fetchall())

cur.execute("SELECT id FROM readings WHERE station_id = 'AWS-001' ORDER BY id")
curr_aws1 = set(row[0] for row in cur.fetchall())

aws1_deleted = bak_aws1 - curr_aws1
print(f'AWS-001 Reading IDs before cleanup: {sorted(list(bak_aws1))}')
print(f'AWS-001 Reading IDs after cleanup: {sorted(list(curr_aws1))}')
print(f'AWS-001 deleted IDs = {sorted(list(aws1_deleted))}')
print(f'AWS-001 sets equal: {bak_aws1 == curr_aws1}')

print('\n=== 6. ANOMALY & CORRECTION HANDLING ===')
cur_bak.execute('SELECT id, reading_id FROM anomalies')
bak_anom = cur_bak.fetchall()
cur.execute('SELECT id, reading_id FROM anomalies')
curr_anom = cur.fetchall()

bak_anom_dict = {row[0]: row[1] for row in bak_anom}
curr_anom_ids = {row[0] for row in curr_anom}
deleted_anomalies = set(bak_anom_dict.keys()) - curr_anom_ids

print(f'Anomalies deleted count: {len(deleted_anomalies)}')
anom_orphans = [a_id for a_id in deleted_anomalies if bak_anom_dict[a_id] not in authorized_ids]
print(f'Anomalies deleted associated with RETAINED readings: {len(anom_orphans)}')
if anom_orphans:
    print(f'Orphan anomalies: {anom_orphans}')

cur_bak.execute('SELECT id, anomaly_id FROM corrections')
bak_corr = cur_bak.fetchall()
cur.execute('SELECT id, anomaly_id FROM corrections')
curr_corr = cur.fetchall()

bak_corr_dict = {row[0]: row[1] for row in bak_corr}
curr_corr_ids = {row[0] for row in curr_corr}
deleted_corrections = set(bak_corr_dict.keys()) - curr_corr_ids

print(f'Corrections deleted count: {len(deleted_corrections)}')
corr_orphans = []
for c_id in deleted_corrections:
    a_id = bak_corr_dict[c_id]
    r_id = bak_anom_dict.get(a_id)
    if r_id not in authorized_ids:
        corr_orphans.append(c_id)
print(f'Corrections deleted associated with RETAINED readings: {len(corr_orphans)}')
if corr_orphans:
    print(f'Orphan corrections: {corr_orphans}')

print('\n=== 7. SQLITE INTEGRITY ===')
cur.execute('PRAGMA integrity_check;')
print(f'integrity_check = {cur.fetchone()[0]}')

print('\n=== 8. BACKUP INTEGRITY ===')
print(f'Backup file exists: {os.path.exists(backup_path)}')
print(f'Backup file size: {os.path.getsize(backup_path)} bytes')
bak_r_count = cur_bak.execute('SELECT COUNT(*) FROM readings').fetchone()[0]
bak_r_max = cur_bak.execute('SELECT MAX(id) FROM readings').fetchone()[0]
print(f'Backup Reading_count: {bak_r_count}')
print(f'Backup Reading_max: {bak_r_max}')

print('\n=== 9. SCHEMA CONSISTENCY ===')
cur.execute('SELECT COUNT(*) FROM anomalies WHERE reading_id NOT IN (SELECT id FROM readings)')
orphan_anom = cur.fetchone()[0]
cur.execute('SELECT COUNT(*) FROM corrections WHERE anomaly_id NOT IN (SELECT id FROM anomalies)')
orphan_corr = cur.fetchone()[0]
print(f'Current orphaned anomalies: {orphan_anom}')
print(f'Current orphaned corrections: {orphan_corr}')

conn.close()
conn_bak.close()

