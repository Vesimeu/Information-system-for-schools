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

    # Создание представлений
    try:
        # Создаем представление для результатов мероприятий
        event_results_view = text("""
        CREATE OR REPLACE VIEW event_results_view AS
        SELECT 
            e.event_id,
            e.name as event_name,
            e.date,
            e.location,
            s.name as sport_name,
            t.first_name || ' ' || t.last_name as teacher_name,
            sch.name as school_name,
            p.first_name || ' ' || p.last_name as participant_name,
            c.name as category_name,
            r.time,
            r.points,
            r.place
        FROM events e
        JOIN sports s ON e.sport_id = s.sport_id
        JOIN teachers t ON e.responsible_id = t.teacher_id
        JOIN results r ON e.event_id = r.event_id
        JOIN participants p ON r.participant_id = p.participant_id
        JOIN schools sch ON p.school_id = sch.school_id
        JOIN categories c ON r.category_id = c.category_id;
        """)
        
        # Создаем представление для очков школ
        school_points_view = text("""
        CREATE OR REPLACE VIEW school_points_view AS
        SELECT 
            s.school_id,
            s.name as school_name,
            SUM(sp.total_points) as total_points
        FROM schools s
        LEFT JOIN school_points sp ON s.school_id = sp.school_id
        GROUP BY s.school_id, s.name;
        """)
        
        # Выполняем создание представлений
        db.session.execute(event_results_view)
        db.session.execute(school_points_view)
        db.session.commit()
        print("Views created successfully")
    except Exception as e:
        print(f"Failed to create views: {e}")
        db.session.rollback()