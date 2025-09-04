from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.crud import user as user_crud
from app.schemas.user import Role

router = APIRouter(prefix="/roles", tags=["roles"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=Role)
def create_role(name: str, description: str = None, db: Session = Depends(get_db)):
    # In a real application, you would check if the user has permission to create roles
    return user_crud.create_role(db=db, role_name=name, description=description)


@router.post("/{user_id}/{role_id}")
def assign_role_to_user(user_id: int, role_id: int, db: Session = Depends(get_db)):
    # In a real application, you would check if the user has permission to assign roles
    user_role = user_crud.assign_role_to_user(db=db, user_id=user_id, role_id=role_id)
    return {"message": "Role assigned successfully", "user_role": user_role}