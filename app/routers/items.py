from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models import Item

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

# Mock database
fake_items_db = {
    1: Item(id=1, name="Laptop", description="A high-performance laptop", price=999.99, tax=199.99),
    2: Item(id=2, name="Smartphone", description="Latest model", price=699.99, tax=139.99),
    3: Item(id=3, name="Headphones", description="Noise-cancelling", price=199.99, tax=39.99)
}

@router.get("/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 10):
    return list(fake_items_db.values())[skip: skip + limit]

@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int, q: Optional[str] = None):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item = fake_items_db[item_id]
    # Just to demonstrate query parameter usage
    if q:
        item.description = f"{item.description} (query: {q})"
        
    return item

@router.post("/", response_model=Item)
async def create_item(item: Item):
    if item.id in fake_items_db:
        raise HTTPException(status_code=400, detail="Item ID already exists")
    
    fake_items_db[item.id] = item
    return item

@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    fake_items_db[item_id] = item
    return item

@router.delete("/{item_id}")
async def delete_item(item_id: int):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    del fake_items_db[item_id]
    return {"message": "Item deleted successfully"}