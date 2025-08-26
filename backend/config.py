import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    DB_USER = os.getenv("DATABASE_USER", "root")
    DB_PASS = os.getenv("DATABASE_PASSWORD", "")
    DB_HOST = os.getenv("DATABASE_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DATABASE_PORT", "3306")
    DB_NAME = os.getenv("DATABASE_NAME", "apidb")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    DEFAULT_PER_PAGE = int(os.getenv("DEFAULT_PER_PAGE", 10))
    MAX_PER_PAGE = int(os.getenv("MAX_PER_PAGE", 50))
