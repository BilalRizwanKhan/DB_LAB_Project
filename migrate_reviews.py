"""
Run this ONCE to create the reviews table:
    python migrate_reviews.py
"""
from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS reviews (
            id          SERIAL PRIMARY KEY,
            property_id INTEGER NOT NULL,
            user_id     INTEGER NOT NULL,
            user_name   VARCHAR NOT NULL,
            rating      INTEGER NOT NULL,
            comment     VARCHAR NOT NULL,
            UNIQUE (user_id, property_id)
        );
    """))
    conn.commit()
    print("✓ reviews table created.")
