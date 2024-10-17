from fastapi import FastAPI
from items_views import router as items_router
from users.views import router as users_router
from api_v1 import router as router_v1
from core.config import settings

app = FastAPI()
app.include_router(items_router)
app.include_router(users_router)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
