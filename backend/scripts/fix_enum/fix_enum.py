"""
Script to fix the enum column in the database
Run this to update the role column to use lowercase values
"""
import sys
import os

# Add parent directory to path to import backend modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database import engine
from sqlalchemy import text


def fix_enum_column():
    """Fix the role column to use lowercase enum values"""
    print("🔧 Fixing role column enum values...")
    
    with engine.connect() as conn:
        # Drop the old column and create new one with correct values
        conn.execute(text("""
            ALTER TABLE users 
            MODIFY COLUMN role 
            ENUM('normal', 'admin', 'empresario') 
            DEFAULT 'normal' NOT NULL
        """))
        conn.commit()
    
    print("✅ Role column fixed successfully!")
    print("Now you can run: python scripts/init_db/init_db.py")


if __name__ == "__main__":
    try:
        fix_enum_column()
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nAlternatively, run this SQL directly in MySQL:")
        print("""
        USE ctp_db;
        ALTER TABLE users 
        MODIFY COLUMN role 
        ENUM('normal', 'admin', 'empresario') 
        DEFAULT 'normal' NOT NULL;
        """)
