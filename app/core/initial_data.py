from app.core.database import SessionLocal
from app.crud.user import create_role

def init_roles():
    try:
        db = SessionLocal()
        try:
            # Create default roles
            admin_role = create_role(db, "Warehouse Administrator", "Can manage inventory and assign roles")
            user_role = create_role(db, "Regular User", "Can view inventory")
            print("Default roles created successfully")
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