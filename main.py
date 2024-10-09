from fastapi import FastAPI, Body, Path
from pydantic import BaseModel, EmailStr
from typing import Annotated

app = FastAPI()


class CreateUser(BaseModel):  # pydantic model for request validation
    email: EmailStr


@app.get("/")
def hello_index():
    return {"message": "Hello index!"}


@app.post("/users_raw_body")  # var as a http raw body
def create_user(email: EmailStr = Body()):
    return {"message": "success", "email": email}


@app.post("/users_json_body")  # var as a http body as a json
def create_user(user: CreateUser):
    return {"message": "success", "email": user.email}


@app.post("/from_path_and_query_and_body/{a}")  # all typs of vars at once
def add(a, b, c=Body()):
    return {"a": a, "b": b, "c": c}


@app.get("/items")
def list_items():
    return ["Item1", "Item2"]


@app.get("/items/latest")
def get_latest_item():
    return {"item": {"id": "0", "name": "latest"}}


@app.get("/items/{item_id}")  # var as a path
def get_item_by_id(
    item_id: Annotated[int, Path(ge=1, lt=1_000_000)]
):  # Annotated for validating value. First one is type, second is a special fastapi obj that allows to pass constraits
    return {"item": {"id": item_id}}


@app.get("/hello")  # var as a query params, and a defoult param "World!"
def hello(name: str = "World!"):
    name = name.strip().title()
    return {"message": f"Hello, {name}!"}
