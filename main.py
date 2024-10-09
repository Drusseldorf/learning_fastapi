from fastapi import FastAPI, Body
from pydantic import BaseModel, EmailStr
from items_views import router as items_router

app = FastAPI()  # should be only in main
app.include_router(items_router)


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


@app.get("/hello")  # var as a query params, and a defoult param "World!"
def hello(name: str = "World!"):
    name = name.strip().title()
    return {"message": f"Hello, {name}!"}
