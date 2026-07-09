"""
Centralized application configuration — all values read from environment.
Sensible local-dev defaults are provided so the app starts without a .env file,
but production MUST override SECRET_KEY and DATABASE_URL.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/circleup",
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-me-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    APP_NAME: str = "CircleUp API"
    API_V1_PREFIX: str = "/api"
    CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "*").split(",")


settings = Settings()