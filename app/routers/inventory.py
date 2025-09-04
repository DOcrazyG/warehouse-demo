from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.crud import inventory as inventory_crud
from app.schemas.inventory import Inventory, InventoryCreate, InventoryUpdate

router = APIRouter(prefix="/inventory", tags=["inventory"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=Inventory)
def create_inventory_item(item: InventoryCreate, db: Session = Depends(get_db)):
    # In a real application, you would check if the user has permission to create inventory items
    return inventory_crud.create_inventory_item(db=db, item=item)


@router.get("/{inventory_id}", response_model=Inventory)
def read_inventory_item(inventory_id: int, db: Session = Depends(get_db)):
    db_item = inventory_crud.get_inventory_item(db, inventory_id=inventory_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get("/", response_model=list[Inventory])
def read_inventory_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = inventory_crud.get_inventory_items(db, skip=skip, limit=limit)
    return items


@router.put("/{inventory_id}", response_model=Inventory)
def update_inventory_item(inventory_id: int, item_update: InventoryUpdate, db: Session = Depends(get_db)):
    db_item = inventory_crud.update_inventory_item(db, inventory_id=inventory_id, item_update=item_update)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.delete("/{inventory_id}", response_model=Inventory)
def delete_inventory_item(inventory_id: int, db: Session = Depends(get_db)):
    db_item = inventory_crud.delete_inventory_item(db, inventory_id=inventory_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.post("/{inventory_id}/stock/in")
def add_stock(inventory_id: int, quantity: int, db: Session = Depends(get_db)):
    # In a real application, you would check if the user has permission to modify stock
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    db_item = inventory_crud.add_stock(db, inventory_id=inventory_id, quantity=quantity)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": f"Added {quantity} units to item {inventory_id}", "item": db_item}


@router.post("/{inventory_id}/stock/out")
def remove_stock(inventory_id: int, quantity: int, db: Session = Depends(get_db)):
    # In a real application, you would check if the user has permission to modify stock
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")
    db_item = inventory_crud.remove_stock(db, inventory_id=inventory_id, quantity=quantity)
    if db_item is None:
        raise HTTPException(status_code=400, detail="Insufficient stock or item not found")
    return {"message": f"Removed {quantity} units from item {inventory_id}", "item": db_item}