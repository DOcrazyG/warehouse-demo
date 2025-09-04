from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
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

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

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
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/users")
async def users_page(request: Request):
    # In a real application, you would fetch users from the database
    users = [
        {"id": 1, "username": "admin", "email": "admin@example.com", "first_name": "Admin", "last_name": "User"},
        {"id": 2, "username": "user1", "email": "user1@example.com", "first_name": "First", "last_name": "User"},
    ]
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/inventory")
async def inventory_page(request: Request):
    # In a real application, you would fetch inventory items from the database
    inventory = [
        {"id": 1, "name": "Laptop", "description": "Gaming laptop", "quantity": 10, "price": 1200.00, "category": "Electronics"},
        {"id": 2, "name": "Desk Chair", "description": "Ergonomic office chair", "quantity": 25, "price": 250.00, "category": "Furniture"},
        {"id": 3, "name": "Monitor", "description": "27-inch 4K monitor", "quantity": 15, "price": 400.00, "category": "Electronics"},
    ]
    return templates.TemplateResponse("inventory.html", {"request": request, "inventory": inventory})