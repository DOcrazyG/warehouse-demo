import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

# Database URL for PostgreSQL
# You should set the DATABASE_URL environment variable
# Example: postgresql://username:password@localhost:5432/warehouse_db
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://warehouse_user:warehouse_password@localhost:5432/warehouse_db"
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()