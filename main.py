from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Item(BaseModel):
    first_name:str
    last_name:str
    email:str
    description: Optional[str] = None


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}/")
def read_item_by_id(item_id: int):
    return { "item_id": item_id}


# @app.post("/items")
# def create_item(item:Item):
#     return item 


@app.post("/items/")
def create_item_param(item: Item):
    item_dict = item.dict()
    if item.first_name and item.last_name:
        detail = item.first_name + item.last_name + " tetsing data"
        item_dict.update({"description": detail})
    return item_dict