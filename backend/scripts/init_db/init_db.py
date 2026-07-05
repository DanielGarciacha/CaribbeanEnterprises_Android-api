"""
Database initialization script
Creates tables and populates with test users
"""
import sys
import os

# Add parent directory to path to import backend modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from database import Base, engine, SessionLocal, User, UserRole
from auth import get_password_hash


def init_database():
    """
    Initialize database with tables and test data
    """
    print("🔧 Creating database tables...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Tables created successfully!")
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_users = db.query(User).count()
        
        if existing_users > 0:
            print(f"⚠️  Database already has {existing_users} user(s)")
            print("Checking which test users need to be created...")
        
        print("\n👤 Creating/Verifying test users...")
        
        # Define test users
        test_users = [
            {
                "username": "admin",
                "email": "admin@test.com",
                "password": "admin123",
                "role": UserRole.ADMIN,
                "description": "Admin User"
            },
            {
                "username": "usuario",
                "email": "usuario@test.com",
                "password": "usuario123",
                "role": UserRole.NORMAL,
                "description": "Normal User"
            },
            {
                "username": "empresario",
                "email": "empresario@test.com",
                "password": "empresario123",
                "role": UserRole.EMPRESARIO,
                "description": "Empresario User"
            }
        ]
        
        created_users = []
        existing_test_users = []
        
        # Check and create each user individually
        for user_data in test_users:
            # Check if user exists by username or email
            existing_user = db.query(User).filter(
                (User.username == user_data["username"]) | 
                (User.email == user_data["email"])
            ).first()
            
            if existing_user:
                existing_test_users.append(user_data["description"])
                print(f"  ⏭️  {user_data['description']} already exists - skipping")
            else:
                # Create new user
                new_user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    hashed_password=get_password_hash(user_data["password"]),
                    role=user_data["role"]
                )
                db.add(new_user)
                created_users.append(user_data["description"])
                print(f"  ✅ Created {user_data['description']}")
        
        # Commit all new users
        if created_users:
            db.commit()
            print(f"\n✅ Successfully created {len(created_users)} new user(s)!")
        else:
            print("\n✅ All test users already exist!")
        
        # Display credentials
        print("\n📋 Test User Credentials:")
        print("=" * 50)
        print("\n--- Admin User ---")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Role: admin")
        print("\n--- Normal User ---")
        print("   Username: usuario")
        print("   Password: usuario123")
        print("   Role: normal")
        print("\n--- Empresario User ---")
        print("   Username: empresario")
        print("   Password: empresario123")
        print("   Role: empresario")
        print("\n" + "=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        return False
        
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 50)
    print("Database Initialization Script")
    print("=" * 50)
    print()
    
    success = init_database()
    
    if success:
        print("\n✅ Database initialization completed successfully!")
        print("\nYou can now:")
        print("1. Start the API server: python main.py")
        print("2. Access API docs: http://localhost:8000/docs")
        print("3. Test login with any of the credentials above")
    else:
        print("\n❌ Database initialization failed!")
        print("Please check the error messages above.")
        sys.exit(1)
