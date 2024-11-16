from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.routes.main import api_router
from app.core.config import settings
from app.core.exceptions import APIException

app = FastAPI(
    title=settings.PROJECT_NAME,
)


@app.exception_handler(APIException)
async def handle_api_exception(request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
    )


app.include_router(api_router, prefix=settings.API_V1_STR)
