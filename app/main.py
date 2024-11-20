from fastapi import FastAPI, HTTPException
from starlette.responses import Response

from app.schemas import Item

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Fast API in Python"}


@app.get("/items/{item_id}")
def get_item(item_id: str):
    return Item(name=item_id)


@app.get("/items/")
def get_items():
    return []


@app.post("/items/", status_code=201)
def create_item(item: Item):
    return item
