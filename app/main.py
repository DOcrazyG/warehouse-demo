from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.routers import users, roles, inventory
from app.core.database import Base, engine
from app.core.init_db import init_db

app = FastAPI(title="Warehouse Management System", 
              description="A demo backend for warehouse management system",
              version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try to create tables, but don't fail if database is not available
try:
    init_db()
    print("Database initialized successfully")
except Exception as e:
    print(f"Warning: Database initialization failed: {e}")
    print("Make sure the database is running and credentials are correct")

# Include routers
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(inventory.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Warehouse Management System API"}