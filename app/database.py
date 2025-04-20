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

    # Определяем SQL для представлений
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

    school_points_view = text("""
    CREATE VIEW public.school_points_view AS
    SELECT 
        s.school_id,
        s.name as school_name,
        COUNT(DISTINCT e.event_id) as events_participated,
        COUNT(r.result_id) as total_results,
        COALESCE(SUM(r.points), 0) as total_points,
        CASE 
            WHEN COUNT(r.result_id) > 0 THEN ROUND(AVG(r.points::numeric), 2)
            ELSE 0 
        END as avg_points
    FROM schools s
    LEFT JOIN participants p ON s.school_id = p.school_id
    LEFT JOIN results r ON p.participant_id = r.participant_id
    LEFT JOIN events e ON r.event_id = e.event_id
    GROUP BY s.school_id, s.name
    ORDER BY total_points DESC;
    """)

    # Принудительно пересоздаем представления
    try:
        # Сначала удаляем существующие представления
        db.session.execute(text("DROP VIEW IF EXISTS school_points_view CASCADE;"))
        db.session.execute(text("DROP VIEW IF EXISTS event_results_view CASCADE;"))
        db.session.commit()
        
        # Создаем представления заново
        db.session.execute(school_points_view)
        db.session.execute(event_results_view)
        db.session.commit()
        print("Views recreated successfully")
    except Exception as e:
        print(f"Failed to recreate views: {e}")
        db.session.rollback()

    # Проверка создания нового представления
    try:
        # Сначала проверяем существование и удаляем старое представление
        db.session.execute(text("""
        DROP VIEW IF EXISTS public.school_points_view CASCADE;
        """))
        db.session.commit()
        
        # Создаем новое представление
        db.session.execute(text("""
        CREATE VIEW public.school_points_view AS
        SELECT 
            s.school_id,
            s.name as school_name,
            COUNT(DISTINCT e.event_id) as events_participated,
            COUNT(r.result_id) as total_results,
            COALESCE(SUM(r.points), 0) as total_points,
            CASE 
                WHEN COUNT(r.result_id) > 0 THEN ROUND(AVG(r.points::numeric), 2)
                ELSE 0 
            END as avg_points
        FROM schools s
        LEFT JOIN participants p ON s.school_id = p.school_id
        LEFT JOIN results r ON p.participant_id = r.participant_id
        LEFT JOIN events e ON r.event_id = e.event_id
        GROUP BY s.school_id, s.name
        ORDER BY total_points DESC;
        """))
        db.session.commit()
        print("School points view created successfully")
    except Exception as e:
        print(f"Error creating school points view: {e}")
        db.session.rollback()