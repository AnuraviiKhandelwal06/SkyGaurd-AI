import sqlite3
import pandas as pd

conn = sqlite3.connect('backend/skyguard.db')
readings = pd.read_sql_query("SELECT * FROM readings ORDER BY station_id, timestamp", conn)

readings['is_dup'] = False
for st in readings['station_id'].unique():
    r_st = readings[readings['station_id'] == st].copy()
    # shift values to check consecutive duplicates
    mask = (r_st['temperature'] == r_st['temperature'].shift(1)) & \
           (r_st['humidity'] == r_st['humidity'].shift(1)) & \
           (r_st['pressure'] == r_st['pressure'].shift(1))
    
    # "A duplicate can only be included if it satisfies the exact consecutive-duplicate definition"
    readings.loc[r_st.index, 'is_dup'] = mask

dup_ids = set(readings[readings['is_dup']]['id'])
print("Consecutive duplicate count:", len(dup_ids))

test_ids = set([38, 39, 48, 49, 53, 54, 76, 77, 78, 79, 80, 81, 85, 86, 87, 99, 100, 101, 102, 107, 108, 109, 110, 111, 112, 113, 114, 119, 120, 121, 122, 123, 124, 125, 126, 194, 214, 215, 216, 218, 219, 220, 226, 227, 228, 237, 238, 239, 245, 246, 247, 249, 250, 251, 257, 258, 259, 261, 262, 263, 268, 269, 270, 271, 272, 273, 280, 281, 282, 284, 285, 286, 288, 289, 290, 296, 297, 298, 300, 301, 302, 308, 309, 310, 312, 313, 314, 320, 321, 322, 324, 325, 326, 332, 333, 334, 336, 337, 338, 339, 340, 341, 343, 344, 345, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 366, 368, 372, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390])

print("Overlap between my dup_ids and the exact 142 IDs:", len(dup_ids.intersection(test_ids)))
print("Dup IDs NOT in the 142 IDs:", dup_ids - test_ids)
