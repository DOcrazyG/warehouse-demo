from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import verify_password, create_access_token
from app.core.auth import get_current_user
from app.crud import user as user_crud
from app.schemas.user import UserLogin, User
from app.schemas.token import Token

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=Token)
def login_for_access_token(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and generate JWT token with 15-minute expiration
    """
    # Get user from database
    user = user_crud.get_user_by_username(db, username=user_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/test-token", response_model=User)
def test_token(current_user: User = Depends(get_current_user)):
    """
    Test endpoint to verify JWT token authentication
    """
    return current_user