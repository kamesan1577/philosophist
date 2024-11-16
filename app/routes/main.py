from fastapi import APIRouter, Security
from app.routes import judge
from app.core.auth import basic_auth

api_router = APIRouter()
api_router.include_router(
    judge.router, tags=["judge"], dependencies=[Security(basic_auth)]
)
