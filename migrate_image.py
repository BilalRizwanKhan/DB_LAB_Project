"""
Run this ONCE to add the image_path column to your existing properties table:
    python migrate_image.py
"""
from database import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE properties ADD COLUMN IF NOT EXISTS image_path VARCHAR;"))
    conn.commit()
    print("✓ image_path column added to properties table.")
