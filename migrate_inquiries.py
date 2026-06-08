"""
Run this ONCE to create the inquiries table:
    python migrate_inquiries.py
"""
from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS inquiries (
            id          SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL,
            buyer_id    INTEGER NOT NULL,
            buyer_name  VARCHAR NOT NULL,
            buyer_email VARCHAR NOT NULL,
            message     VARCHAR NOT NULL,
            status      VARCHAR DEFAULT 'pending',
            reply       VARCHAR
        );
    """))
    conn.commit()
    print("✓ inquiries table created.")
