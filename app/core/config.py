from typing import List, Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
    )
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["development", "production"] = "development"
    PROJECT_NAME: str

    OPENAI_API_KEY: str
    BASIC_AUTH_USERNAME: str
    BASIC_AUTH_PASSWORD: str

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    REDIS_URL: Optional[str] = None
    REDIS_TOKEN: Optional[str] = None

    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    CORS_ALLOW_METHODS: List[str] = ["*"]

    @property
    def cors_origins(self) -> List[str]:
        """
        開発環境と本番環境で異なるCORS設定を返す
        """
        if self.ENVIRONMENT == "development":
            return ["*"]
        return self.CORS_ORIGINS


settings = Settings()
