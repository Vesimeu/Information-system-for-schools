# app/routes.py
from flask import render_template, request, redirect, url_for, flash
from app import db
from app.models import (
    School, Class, Participant, Sport, Event, Teacher, 
    Category, EventResultsView, SchoolPointsView, EventParticipant
)
from app.forms import (
    SchoolForm, ClassForm, ParticipantForm, TeacherForm,
    EventCreationForm, SportForm, CategoryForm
)
from datetime import datetime
from sqlalchemy.sql import text

def register_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    # Основные сущности
    @app.route("/schools")
    def schools():
        schools = School.query.all()
        return render_template("schools.html", schools=schools)

    @app.route("/add_school", methods=["GET", "POST"])
    def add_school():
        form = SchoolForm()
        if form.validate_on_submit():
            school = School(
                name=form.name.data,
                address=form.address.data,
                contact_phone=form.contact_phone.data
            )
            db.session.add(school)
            db.session.commit()
            flash('Школа успешно добавлена', 'success')
            return redirect(url_for('schools'))
        return render_template("add_school.html", form=form)

    @app.route("/sports")
    def sports():
        sports = Sport.query.all()
        return render_template("sports.html", sports=sports)

    @app.route("/add_sport", methods=["GET", "POST"])
    def add_sport():
        form = SportForm()
        if form.validate_on_submit():
            sport = Sport(
                name=form.name.data,
                description=form.description.data
            )
            db.session.add(sport)
            db.session.commit()
            flash('Вид спорта успешно добавлен', 'success')
            return redirect(url_for('sports'))
        return render_template("add_sport.html", form=form)

    @app.route("/teachers")
    def teachers():
        teachers = Teacher.query.all()
        return render_template("teachers.html", teachers=teachers)

    @app.route("/add_teacher", methods=["GET", "POST"])
    def add_teacher():
        form = TeacherForm()
        form.school_id.choices = [(s.school_id, s.name) for s in School.query.all()]
        if form.validate_on_submit():
            teacher = Teacher(
                school_id=form.school_id.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                phone=form.phone.data
            )
            db.session.add(teacher)
            db.session.commit()
            flash('Учитель успешно добавлен', 'success')
            return redirect(url_for('teachers'))
        return render_template("add_teacher.html", form=form)

    @app.route("/classes")
    def classes():
        classes = Class.query.all()
        return render_template("classes.html", classes=classes)

    @app.route("/add_class", methods=["GET", "POST"])
    def add_class():
        form = ClassForm()
        form.school_id.choices = [(s.school_id, s.name) for s in School.query.all()]
        form.teacher_id.choices = [(t.teacher_id, f"{t.first_name} {t.last_name}")
                                   for t in Teacher.query.all()]

        if form.validate_on_submit():
            class_ = Class(
                school_id=form.school_id.data,
                name=form.name.data,
                year=form.year.data,
                teacher_id=form.teacher_id.data
            )
            db.session.add(class_)
            db.session.commit()
            flash('Класс успешно добавлен', 'success')
            return redirect(url_for('classes'))
        return render_template("add_class.html", form=form)

    @app.route("/participants")
    def participants():
        participants = Participant.query.all()
        return render_template("participants.html", participants=participants)

    @app.route("/add_participant", methods=["GET", "POST"])
    def add_participant():
        form = ParticipantForm()
        form.school_id.choices = [(s.school_id, s.name) for s in School.query.all()]
        form.class_id.choices = [(c.class_id, c.name) for c in Class.query.all()]
        if form.validate_on_submit():
            participant = Participant(
                school_id=form.school_id.data,
                class_id=form.class_id.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                birth_date=form.birth_date.data,
                gender=form.gender.data
            )
            db.session.add(participant)
            db.session.commit()
            flash('Участник успешно добавлен', 'success')
            return redirect(url_for('participants'))
        return render_template("add_participant.html", form=form)

    # Мероприятия
    @app.route("/events")
    def events():
        events = Event.query.options(
            db.joinedload(Event.sport),
            db.joinedload(Event.responsible)
        ).all()
        return render_template("events.html", events=events)

    @app.route("/create_event", methods=["GET", "POST"])
    def create_event():
        form = EventCreationForm()
        
        # Заполняем выпадающие списки
        form.sport_id.choices = [(s.sport_id, s.name) for s in Sport.query.all()]
        form.responsible_id.choices = [(t.teacher_id, f"{t.first_name} {t.last_name}") 
                                     for t in Teacher.query.all()]
        form.participants.choices = [(p.participant_id, f"{p.first_name} {p.last_name}") 
                                   for p in Participant.query.all()]
        form.categories.choices = [(c.category_id, c.name) for c in Category.query.all()]
        
        if form.validate_on_submit():
            try:
                # Создаем мероприятие
                event = Event(
                    name=form.name.data,
                    date=form.date.data,
                    location=form.location.data,
                    sport_id=form.sport_id.data,
                    responsible_id=form.responsible_id.data,
                    distance=form.distance.data
                )
                db.session.add(event)
                db.session.flush()  # Получаем event_id
                
                # Добавляем участников
                for participant_id in form.participants.data:
                    event_participant = EventParticipant(
                        event_id=event.event_id,
                        participant_id=participant_id,
                        registration_date=datetime.now()
                    )
                    db.session.add(event_participant)
                
                db.session.commit()
                flash('Мероприятие успешно создано', 'success')
                return redirect(url_for('events'))
            except Exception as e:
                db.session.rollback()
                flash(f'Ошибка при создании мероприятия: {str(e)}', 'error')
        
        return render_template("create_event.html", form=form)

    # Представления
    @app.route("/event_results")
    def event_results():
        results = EventResultsView.query.all()
        return render_template("event_results.html", results=results)

    @app.route("/school_points")
    def school_points():
        points = SchoolPointsView.query.all()
        return render_template("school_points.html", points=points)

    @app.route("/categories")
    def categories():
        categories = Category.query.all()
        return render_template("categories.html", categories=categories)

    @app.route("/add_category", methods=["GET", "POST"])
    def add_category():
        form = CategoryForm()
        if form.validate_on_submit():
            category = Category(
                name=form.name.data,
                min_age=form.min_age.data,
                max_age=form.max_age.data,
                gender=form.gender.data if form.gender.data else None
            )
            db.session.add(category)
            db.session.commit()
            flash('Категория успешно добавлена', 'success')
            return redirect(url_for('categories'))
        return render_template("add_category.html", form=form)