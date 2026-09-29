import sqlite3
import pandas as pd

conn = sqlite3.connect('backend/skyguard.db')
readings = pd.read_sql_query("SELECT * FROM readings", conn)

dup_ids = set([347, 366, 368]) # wait, I can just use the 124 dup IDs
readings['is_dup'] = False
for st in readings['station_id'].unique():
    r_st = readings[readings['station_id'] == st].copy()
    mask = (r_st['temperature'] == r_st['temperature'].shift(1)) & \
           (r_st['humidity'] == r_st['humidity'].shift(1)) & \
           (r_st['pressure'] == r_st['pressure'].shift(1))
    readings.loc[r_st.index, 'is_dup'] = mask

dup_124 = set(readings[(readings['is_dup']) & (readings['station_id'] != 'AWS-001')]['id'])
ids_142 = set([38, 39, 48, 49, 53, 54, 76, 77, 78, 79, 80, 81, 85, 86, 87, 99, 100, 101, 102, 107, 108, 109, 110, 111, 112, 113, 114, 119, 120, 121, 122, 123, 124, 125, 126, 194, 214, 215, 216, 218, 219, 220, 226, 227, 228, 237, 238, 239, 245, 246, 247, 249, 250, 251, 257, 258, 259, 261, 262, 263, 268, 269, 270, 271, 272, 273, 280, 281, 282, 284, 285, 286, 288, 289, 290, 296, 297, 298, 300, 301, 302, 308, 309, 310, 312, 313, 314, 320, 321, 322, 324, 325, 326, 332, 333, 334, 336, 337, 338, 339, 340, 341, 343, 344, 345, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 366, 368, 372, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390])

test_32 = ids_142 - dup_124 # this gives the 18 pure test ids
print("Pure TEST_ONLY (18 ids):", test_32)

# But wait, we need the 14 overlap IDs too! 
# Let's just print out all ids in 142 that have source != 'physical_sensor' ? No, some test_set are physical_sensor?
# Let's print out the properties of the 18 pure test IDs.
print(readings[readings['id'].isin(test_32)][['id', 'station_id', 'timestamp', 'source']])

