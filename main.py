from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def hello_index():
    return {"message": "Hello index!"}


@app.get("/items")
def list_items():
    return ["Item1", "Item2"]


@app.get("/item/{item_id}")
def get_item_by_id(item_id: int):
    return {"item": {"id": item_id}}
