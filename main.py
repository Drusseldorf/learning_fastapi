from fastapi import FastAPI, Body
from pydantic import BaseModel, EmailStr
from items_views import router as items_router
from users.views import router as users_router

app = FastAPI()
app.include_router(items_router)
app.include_router(users_router)


@app.get("/")
def hello_index():
    return {"message": "Hello index!"}
