from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import os

from app.core.config import Settings
from app.core.config import settings

security = HTTPBasic()


def basic_auth(credentials: HTTPBasicCredentials = Security(security)):
    correct_username = secrets.compare_digest(
        credentials.username, settings.BASIC_AUTH_USERNAME
    )
    correct_password = secrets.compare_digest(
        credentials.password, settings.BASIC_AUTH_PASSWORD
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
