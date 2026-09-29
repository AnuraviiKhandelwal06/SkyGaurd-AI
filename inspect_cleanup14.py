import sqlite3
import pandas as pd

conn = sqlite3.connect('backend/skyguard.db')
readings = pd.read_sql_query("SELECT * FROM readings", conn)

# 1. Duplicates
readings['is_dup'] = False
for st in readings['station_id'].unique():
    r_st = readings[readings['station_id'] == st].copy()
    mask = (r_st['temperature'] == r_st['temperature'].shift(1)) & \
           (r_st['humidity'] == r_st['humidity'].shift(1)) & \
           (r_st['pressure'] == r_st['pressure'].shift(1))
    readings.loc[r_st.index, 'is_dup'] = mask

dup_ids = set(readings[(readings['is_dup']) & (readings['station_id'] != 'AWS-001')]['id'])

# 2. Test Only (ID >= 340 ? No, wait. Some earlier ones? No, the list of 142 IDs has IDs like 38, 39, 48... )
# WAIT! The 142 IDs from my recovered list: 38, 39, 48, 49... 
# Are 38, 39, 48 duplicates?! Yes! They are in dup_ids!
# So 124 of the 142 IDs are JUST duplicates!
# And the remaining 18 IDs are the pure TEST_ONLY IDs.
# What are the 18 IDs? {347, 348, 350, 351, 352, 353, 354, 356, 357, 358, 359, 360, 361, 362, 363, 375, 376, 377, 378, 380, 381, 382, 383} -> wait, that's 23 IDs, not 18!
# Let me just check if the rule is simply: DUPLICATES + SOME SPECIFIC FUTURE DATES?
# "TEST ROWS (read-only): list every reading with timestamp later than current UTC now... plus any other row that looks mock-generated"
# Wait! In the previous transcript I printed exactly how I computed the 142 IDs!
