# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # Prefer full DB URL if present (Render often provides this)
    DATABASE_URL = (
        os.getenv("DATABASE_URL")
        or os.getenv("EXTERNAL_DATABASE_URL")
        or os.getenv("POSTGRES_URL")
        or os.getenv("DATABASE_EXTERNAL_URL")   # sometimes named differently
    )

    if DATABASE_URL:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Support two naming conventions:
        DB_USER = os.getenv("DB_USER") or os.getenv("DATABASE_USER")
        DB_PASS = os.getenv("DB_PASSWORD") or os.getenv("DATABASE_PASSWORD")
        DB_HOST = os.getenv("DB_HOST") or os.getenv("DATABASE_HOST") or "127.0.0.1"
        DB_PORT = os.getenv("DB_PORT") or os.getenv("DATABASE_PORT") or "5432"
        DB_NAME = os.getenv("DB_NAME") or os.getenv("DATABASE_NAME")

        SQLALCHEMY_DATABASE_URI = (
            f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    DEFAULT_PER_PAGE = int(os.getenv("DEFAULT_PER_PAGE", 10))
    MAX_PER_PAGE = int(os.getenv("MAX_PER_PAGE", 50))
