# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:123123@localhost:5432/postgres")
    SQLALCHEMY_TRACK_MODIFICATIONS = False