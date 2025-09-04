# Warehouse Management System Demo

A backend demo for warehouse management system built with Python, FastAPI, SQLAlchemy, and PostgreSQL.

## Features

1. User Management
   - User registration
   - User login
   - User information modification
   - User deletion

2. Role Management
   - Role creation
   - Role modification
   - Role deletion
   - Assign roles to users
   - Main roles: Warehouse Administrator, Regular User

3. Inventory Management
   - Add inventory items
   - Update inventory items
   - View inventory
   - Stock in (add quantity)
   - Stock out (remove quantity)

4. Role-Based Access Control
   - Regular users can only view inventory
   - Admin users can manage users and inventory (stock in/out)

## Technology Stack

- Programming Language: Python
- Database: PostgreSQL
- Web Framework: FastAPI
- ORM Library: SQLAlchemy
- Template Engine: Jinja2

## Installation

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Set up your PostgreSQL database:

   First, make sure PostgreSQL is installed and running on your system.
   
   Then create a database and user:
   ```sql
   CREATE USER warehouse_user WITH PASSWORD 'warehouse_password';
   CREATE DATABASE warehouse_db OWNER warehouse_user;
   ```

3. Set the DATABASE_URL environment variable:
   ```bash
   export DATABASE_URL="postgresql://warehouse_user:warehouse_password@localhost:5432/warehouse_db"
   ```

4. Initialize the database:
   ```
   python -m app.core.init_db
   ```

## Running the Application

To run the application, use:
```
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Web Interface

The application includes a web interface using Jinja2 templates:
- Home page: `http://localhost:8000/`
- Login page: `http://localhost:8000/login`
- Registration page: `http://localhost:8000/register`
- Users page (admin only): `http://localhost:8000/users`
- Inventory page: `http://localhost:8000/inventory`

## Authentication and Authorization

- Regular users can only view inventory information after logging in
- Admin users (like 'admin') can manage users and perform stock operations
- In a real application, authentication would be implemented with proper session management or JWT tokens

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
app/
├── core/           # Database configuration and initialization
├── crud/           # CRUD operations
├── models/         # Database models
├── routers/        # API routes
├── schemas/        # Pydantic models for data validation
├── templates/      # Jinja2 templates for web interface
├── static/         # Static files (CSS, JS, images)
├── utils/          # Utility functions
└── main.py         # Main application file
```