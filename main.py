from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Item(BaseModel):
    id : int
    name : str
    description : str
    price : float
    quantity : int
    
products = [
    Item(id=1, name="Laptop", description="A high-performance laptop", price=999.99, quantity=10),
    Item(id=2, name="Smartphone", description="A powerful smartphone", price=499.99, quantity=20),
    Item(id=3, name="Headphones", description="Noise-cancelling headphones", price=199.99, quantity=15),
    Item(id=4, name="Smartwatch", description="A stylish smartwatch", price=299.99, quantity=5),
    Item(id=5, name="Tablet", description="A versatile tablet", price=399.99, quantity=8)
]
 
@app.get("/")
def read_root():
    return "Welcome to FastAPI!"

@app.get("/items/")
def get_all_items():
    return products

@app.get("/item/{item_id}")
def get_item(item_id: int):
    for item in products:
        if item.id == item_id:
            return item
    return {"error": "Item not found"}

@app.post("/item/")
def create_item(item: Item):
    products.append(item)
    return item