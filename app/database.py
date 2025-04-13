# app/database.py
from . import db
from sqlalchemy import inspect
from sqlalchemy.sql import text


def init_db():
    inspector = inspect(db.engine)

    # Список всех таблиц
    tables = [
        "schools", "classes", "participants", "sports", "ranks",
        "participant_ranks", "events", "teachers", "event_participants",
        "results", "school_points", "categories", "logs"
    ]

    # Проверяем, существуют ли все таблицы
    missing_tables = [table for table in tables if not inspector.has_table(table)]

    if missing_tables:
        print(f"Creating tables: {', '.join(missing_tables)}...")
        db.create_all()
    else:
        print("All tables already exist.")

    # Тестовое подключение
    try:
        result = db.session.execute(text("SELECT 1"))
        print("Database connection successful:", result.fetchone())
    except Exception as e:
        print("Database connection failed:", str(e))