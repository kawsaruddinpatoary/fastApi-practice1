from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Item(BaseModel):
    id : int | None = None
    name : str | None = None 
    description : str | None = None
    price : float | None = None 
    quantity : int | None = None
    
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

@app.put("/item/{item_id}")
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(products):
        if item.id == item_id:
            products[index] = updated_item
            return updated_item
    return {"error": "Item not found"}

@app.patch("/item/{item_id}")
def partial_update_item(item_id: int, updated_fields: Item):
    for index, item in enumerate(products):
        if item.id == item_id:
            updated_item = products[index]
            if updated_fields.name is not None:
                updated_item.name = updated_fields.name
            if updated_fields.description is not None:
                updated_item.description = updated_fields.description
            if updated_fields.price is not None:
                updated_item.price = updated_fields.price
            if updated_fields.quantity is not None:
                updated_item.quantity = updated_fields.quantity
            products[index] = updated_item
            return updated_item
    return {"error": "Item not found"}

@app.delete("/item/{item_id}")
def delete_item(item_id: int):
    for index, item in enumerate(products):
        if item.id == item_id:
            del products[index]
            return {"message": "Item deleted"}
    return {"error": "Item not found"}