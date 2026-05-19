import json 
import os
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Item(BaseModel):
    id : int | None = None
    name : str | None = None 
    description : str | None = None
    price : float | None = None 
    quantity : int | None = None
    
    
FILE_PATH = "products.json"

# Helper function to read data from the JSON file
def load_products() -> list:
    with open(FILE_PATH, "r") as file:
        return json.load(file)

# Helper function to write data back to the JSON file
def save_products(data: list):
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)
    
 
@app.get("/")
def read_root():
    return "Welcome to FastAPI!"

@app.get("/items/")
def get_all_items():
    return load_products()

@app.get("/item/{item_id}")
def get_item(item_id: int):
    products_data = load_products()
    for item in products_data:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}

@app.post("/item/")
def create_item(item: Item):
    products_data = load_products()
    new_item = item.dict()
    products_data.append(new_item)
    save_products(products_data)
    return item

@app.put("/item/{item_id}")
def update_item(item_id: int, updated_item: Item):
    products_data = load_products()
    for index, item in enumerate(products_data):
        if item["id"] == item_id:
            updated_dict = updated_item.dict()
            products_data[index] = updated_dict
            save_products(products_data)
            return updated_item
    return {"error": "Item not found"}

@app.patch("/item/{item_id}")
def partial_update_item(item_id: int, updated_fields: Item):
    products_data = load_products()
    for index, item in enumerate(products_data):
        if item["id"] == item_id:
            updated_item = products_data[index]
            if updated_fields.name is not None:
                updated_item["name"] = updated_fields.name
            if updated_fields.description is not None:
                updated_item["description"] = updated_fields.description
            if updated_fields.price is not None:
                updated_item["price"] = updated_fields.price
            if updated_fields.quantity is not None:
                updated_item["quantity"] = updated_fields.quantity
            products_data[index] = updated_item
            save_products(products_data)
            return updated_item
    return {"error": "Item not found"}

@app.delete("/item/{item_id}")
def delete_item(item_id: int):
    products_data = load_products()
    for index, item in enumerate(products_data):
        if item["id"] == item_id:
            del products_data[index]
            save_products(products_data)
            return {"message": "Item deleted"}
    return {"error": "Item not found"}