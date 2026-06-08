"""
Run this ONCE to add profile columns to the users table:
    python migrate_profile.py
"""
from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS phone  VARCHAR;"))
    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS city   VARCHAR;"))
    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS bio    VARCHAR;"))
    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar VARCHAR;"))
    conn.commit()
    print("✓ Profile columns added to users table.")
