from fastapi import FastAPI
from fastapi.routing import APIRouter
from pydantic import BaseModel
import uvicorn
from src.config import settings
from src.router.user import router as user_router
from src.router.moneyBox import router as moneybox_router

app = FastAPI(openapi_url=f"{settings.BASE_ROUTE_PATH}/openapi.json", docs_url=f"{settings.BASE_ROUTE_PATH}/docs")

router = APIRouter(prefix=settings.BASE_ROUTE_PATH)

# router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
# router.include_router(users.router, prefix="/users", tags=["Tasks"])
router.include_router(user_router, prefix="/user", tags=["users"])
router.include_router(moneybox_router, prefix="/moneybox", tags=["moneybox"])

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reloade=True)

