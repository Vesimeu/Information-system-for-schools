from app import create_app, db
from sqlalchemy import inspect, text

app = create_app()

with app.app_context():
    # Получаем инспектор для работы с метаданными БД
    inspector = inspect(db.engine)

    # Удаляем все представления вручную перед удалением таблиц
    for view_name in inspector.get_view_names(schema='public'):
        db.session.execute(text(f'DROP VIEW IF EXISTS public.{view_name} CASCADE'))

    # Теперь можем безопасно удалять таблицы
    db.drop_all()

    # Создаем все таблицы заново
    db.create_all()

    db.session.commit()