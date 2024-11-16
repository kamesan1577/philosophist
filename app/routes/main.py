from fastapi import APIRouter
from app.routes import judge

api_router = APIRouter()
api_router.include_router(judge.router, tags=["judge"])
