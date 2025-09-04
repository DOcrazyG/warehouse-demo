from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate, InventoryUpdate
from typing import List, Optional


def get_inventory_item(db: Session, inventory_id: int):
    return db.query(Inventory).filter(Inventory.id == inventory_id).first()


def get_inventory_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Inventory).offset(skip).limit(limit).all()


def create_inventory_item(db: Session, item: InventoryCreate):
    db_item = Inventory(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_inventory_item(db: Session, inventory_id: int, item_update: InventoryUpdate):
    db_item = get_inventory_item(db, inventory_id)
    if db_item:
        update_data = item_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_inventory_item(db: Session, inventory_id: int):
    db_item = get_inventory_item(db, inventory_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item


def add_stock(db: Session, inventory_id: int, quantity: int):
    db_item = get_inventory_item(db, inventory_id)
    if db_item:
        db_item.quantity += quantity
        db.commit()
        db.refresh(db_item)
    return db_item


def remove_stock(db: Session, inventory_id: int, quantity: int):
    db_item = get_inventory_item(db, inventory_id)
    if db_item and db_item.quantity >= quantity:
        db_item.quantity -= quantity
        db.commit()
        db.refresh(db_item)
        return db_item
    return None