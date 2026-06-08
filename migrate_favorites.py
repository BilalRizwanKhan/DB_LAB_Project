"""
Run this ONCE to create the favorites table:
    python migrate_favorites.py
"""
from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS favorites (
            id          SERIAL PRIMARY KEY,
            user_id     INTEGER NOT NULL,
            property_id INTEGER NOT NULL,
            UNIQUE (user_id, property_id)
        );
    """))
    conn.commit()
    print("✓ favorites table created.")
