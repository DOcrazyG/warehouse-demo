from app.core.database import SessionLocal
from app.crud.user import create_role, create_user
from app.schemas.user import UserCreate

def init_roles():
    try:
        db = SessionLocal()
        try:
            # Create default roles
            admin_role = create_role(db, "Warehouse Administrator", "Can manage inventory and assign roles")
            user_role = create_role(db, "Regular User", "Can view inventory")
            print("Default roles created successfully")
            
            # Create default admin user
            admin_user = UserCreate(
                username="admin",
                email="admin@example.com",
                password="admin123",
                first_name="Admin",
                last_name="User"
            )
            
            # Check if admin user already exists
            from app.crud.user import get_user_by_username
            existing_user = get_user_by_username(db, "admin")
            if not existing_user:
                create_user(db, admin_user)
                print("Default admin user created successfully")
            else:
                print("Admin user already exists")
            
            return [admin_role, user_role]
        except Exception as e:
            print(f"Error creating default roles: {e}")
        finally:
            db.close()
    except Exception as e:
        print(f"Error connecting to database: {e}")
        print("Make sure the database is running and credentials are correct")

if __name__ == "__main__":
    init_roles()