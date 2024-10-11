from contextlib import asynccontextmanager
from core.models import Base, db_helper
from fastapi import FastAPI
from items_views import router as items_router
from users.views import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # define this startup and shutdown logic using the lifespan parameter of the FastAPI app, and a "context manager".
    # This code will be executed before the application starts taking requests, during the startup.
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(items_router)
app.include_router(users_router)
