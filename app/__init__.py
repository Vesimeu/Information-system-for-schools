# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        # Инициализация базы данных
        from .database import init_db
        init_db()

        # Регистрация маршрутов
        from .routes import register_routes
        register_routes(app)

    return app