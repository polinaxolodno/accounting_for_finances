from fastapi import FastAPI
from fastapi.routing import APIRouter
from pydantic import BaseModel
import uvicorn
from src.config import settings
from src.router.user import router as user_router
from src.router.moneyBox import router as moneybox_router
from src.router.auth import router as auth_router
from src.router.dailyBudget import router as dailyBudget_router

app = FastAPI(openapi_url=f"{settings.BASE_ROUTE_PATH}/openapi.json", docs_url=f"{settings.BASE_ROUTE_PATH}/docs")

router = APIRouter(prefix=settings.BASE_ROUTE_PATH)

router.include_router(user_router, prefix="/user", tags=["UsErs"])
router.include_router(moneybox_router, prefix="/moneybox", tags=["mOnEYbOx"])
router.include_router(auth_router, prefix="/auth", tags=["AUth"])
router.include_router(dailyBudget_router, prefix="/dailybudget", tags=["dailyBudget"])

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reloade=True)
