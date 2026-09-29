from sqlalchemy import create_engine, text
engine = create_engine('sqlite:///backend/skyguard.db')
with engine.begin() as conn:
    conn.execute(text('''
    DELETE FROM corrections 
    WHERE anomaly_id IN (
        SELECT id FROM anomalies WHERE status IN ('resolved', 'warning', 'genuine_event')
    )
    '''))
