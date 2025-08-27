# backend/config.py
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # Prefer full DB URL if present
    DATABASE_URL = (
        os.getenv("DATABASE_URL")
        or os.getenv("EXTERNAL_DATABASE_URL")
        or os.getenv("POSTGRES_URL")
        or os.getenv("DATABASE_EXTERNAL_URL")
    )

    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Fallback with defaults (no KeyErrors!)
        DB_USER = os.getenv("DB_USER", "postgres")
        DB_PASS = os.getenv("DB_PASSWORD", "postgres")
        DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
        DB_PORT = os.getenv("DB_PORT", "5432")
        DB_NAME = os.getenv("DB_NAME", "testdb")

        SQLALCHEMY_DATABASE_URI = (
            f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # External API keys
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", None)
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)

    # Pagination
    DEFAULT_PER_PAGE = int(os.getenv("DEFAULT_PER_PAGE", 10))
    MAX_PER_PAGE = int(os.getenv("MAX_PER_PAGE", 50))
