from app.core.database import Base, engine
from app.models.user import User, Role, UserRole
from app.models.inventory import Inventory


def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    try:
        init_db()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        print("Make sure the database is running and credentials are correct")