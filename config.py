# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:123123@localhost:5432/postgres?options=-csearch_path=public")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    # Проверка загрузки SECRET_KEY
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")