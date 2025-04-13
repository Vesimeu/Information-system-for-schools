# app/database.py
from . import db
from .models import School
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
    missing_tables = [table for table in tables if not inspector.has_table(table, schema="public")]

    if missing_tables:
        print(f"Creating tables: {', '.join(missing_tables)}...")
        try:
            db.create_all()
            db.session.commit()
            print("Tables created successfully.")

            # Добавляем тестовые данные
            if not School.query.first():
                db.session.add(School(name="School №1", address="123 Main St", contact_phone="+123456789"))
                db.session.add(School(name="School №2", address="456 Oak St", contact_phone="+987654321"))
                db.session.commit()
                print("Test data added.")
        except Exception as e:
            print(f"Failed to create tables: {e}")
            db.session.rollback()
    else:
        print("All tables already exist.")

    # Тестовое подключение
    try:
        result = db.session.execute(text("SELECT 1"))
        print("Database connection successful:", result.fetchone())
    except Exception as e:
        print("Database connection failed:", str(e))

    # Проверка существования таблиц
    try:
        result = db.session.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        existing_tables = [row[0] for row in result]
        print("Existing tables in schema 'public':", existing_tables)
    except Exception as e:
        print("Failed to list tables:", str(e))