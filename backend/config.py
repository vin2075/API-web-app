import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_NAME = os.getenv("DB_NAME")

    # PostgreSQL URI
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    DEFAULT_PER_PAGE = int(os.getenv("DEFAULT_PER_PAGE", 10))
    MAX_PER_PAGE = int(os.getenv("MAX_PER_PAGE", 50))
