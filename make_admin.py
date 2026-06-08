"""
Run this once to make a user an admin:
    python make_admin.py your@email.com
"""
import sys
from database import SessionLocal
import models

def make_admin(email: str):
    db = SessionLocal()
    user = db.query(models.User).filter_by(email=email).first()
    if not user:
        print(f"No user found with email: {email}")
        return
    user.is_admin = True
    db.commit()
    print(f"✓ {user.name} ({email}) is now an admin.")
    db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python make_admin.py your@email.com")
    else:
        make_admin(sys.argv[1])
