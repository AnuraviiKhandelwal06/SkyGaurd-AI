import sqlite3

conn = sqlite3.connect('backend/skyguard.db')
cur = conn.cursor()

authorized_ids = (38, 39, 48, 49, 53, 54, 76, 77, 78, 79, 80, 81, 85, 86, 87, 99, 100, 101, 102, 107, 108, 109, 110, 111, 112, 113, 114, 119, 120, 121, 122, 123, 124, 125, 126, 194, 214, 215, 216, 218, 219, 220, 226, 227, 228, 237, 238, 239, 245, 246, 247, 249, 250, 251, 257, 258, 259, 261, 262, 263, 268, 269, 270, 271, 272, 273, 280, 281, 282, 284, 285, 286, 288, 289, 290, 296, 297, 298, 300, 301, 302, 308, 309, 310, 312, 313, 314, 320, 321, 322, 324, 325, 326, 332, 333, 334, 336, 337, 338, 339, 340, 341, 343, 344, 345, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 366, 368, 372, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390)

cur.execute(f"SELECT COUNT(*) FROM anomalies WHERE reading_id IN {authorized_ids}")
a_count = cur.fetchone()[0]

cur.execute(f"SELECT COUNT(*) FROM corrections WHERE anomaly_id IN (SELECT id FROM anomalies WHERE reading_id IN {authorized_ids})")
c_count = cur.fetchone()[0]

print("Anomalies to be cascaded:", a_count)
print("Corrections to be cascaded:", c_count)

