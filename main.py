from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# Simulando um banco de dados em memória
fake_db = []

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    fake_db.append(item)
    return item

@app.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 10):
    return fake_db[skip: skip + limit]

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    for item in fake_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    for idx, db_item in enumerate(fake_db):
        if db_item.id == item_id:
            fake_db[idx] = item
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    for idx, item in enumerate(fake_db):
        if item.id == item_id:
            return fake_db.pop(idx)
    raise HTTPException(status_code=404, detail="Item not found")
