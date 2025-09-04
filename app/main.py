from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os
from app.routers import users, roles, inventory
from app.core.database import SessionLocal
from app.core.database import Base, engine
from app.core.init_db import init_db
from app.crud import user as user_crud, inventory as inventory_crud

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

# Security
security = HTTPBearer()

# Try to create tables, but don't fail if database is not available
try:
    init_db()
    print("Database initialized successfully")
except Exception as e:
    print(f"Warning: Database initialization failed: {e}")
    print("Make sure the database is running and credentials are correct")

# Include API routers
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(inventory.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/users")
async def users_page(request: Request, db: Session = Depends(get_db)):
    users = user_crud.get_users(db)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/inventory")
async def inventory_page(request: Request, db: Session = Depends(get_db)):
    inventory_items = inventory_crud.get_inventory_items(db)
    return templates.TemplateResponse("inventory.html", {"request": request, "inventory": inventory_items})