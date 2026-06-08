"""
Run this ONCE to create the appointments table:
    python migrate_appointments.py
"""
from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS appointments (
            id          SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL,
            user_id     INTEGER NOT NULL,
            user_name   VARCHAR NOT NULL,
            user_email  VARCHAR NOT NULL,
            visit_date  VARCHAR NOT NULL,
            visit_time  VARCHAR NOT NULL,
            note        VARCHAR,
            status      VARCHAR DEFAULT 'pending'
        );
    """))
    conn.commit()
    print("✓ appointments table created.")
