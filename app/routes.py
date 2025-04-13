# app/routes.py
from flask import render_template, request, redirect, url_for
from . import db
from .models import School, Class, Participant, Sport, Rank, ParticipantRank, Event, Teacher, EventParticipant, Result, \
    SchoolPoint, Category, Log
from .forms import SchoolForm, ClassForm, ParticipantForm, SportForm, RankForm, ParticipantRankForm, EventForm, \
    TeacherForm, EventParticipantForm, ResultForm, SchoolPointForm, CategoryForm, LogForm
from sqlalchemy.exc import ProgrammingError
from datetime import datetime
from sqlalchemy.sql import text


def register_routes(app):
    @app.route("/")
    def index():
        data = {}
        models = [School, Class, Participant, Sport, Rank, ParticipantRank, Event, Teacher, EventParticipant, Result,
                  SchoolPoint, Category, Log]
        for model in models:
            try:
                data[model.__tablename__] = model.query.all()
            except ProgrammingError as e:
                print(f"Query failed for {model.__tablename__}: {e}")
                data[model.__tablename__] = []
        return render_template("index.html", data=data)

    @app.route("/add_school", methods=["GET", "POST"])
    def add_school():
        form = SchoolForm()
        if form.validate_on_submit():
            try:
                school = School(
                    name=form.name.data,
                    address=form.address.data,
                    contact_phone=form.contact_phone.data
                )
                db.session.add(school)
                db.session.commit()
                return redirect(url_for("index"))
            except Exception as e:
                print(f"Failed to add school: {e}")
                db.session.rollback()
                form.errors["submit"] = [str(e)]
        return render_template("add_school.html", form=form)

    @app.route("/add_class", methods=["GET", "POST"])
    def add_class():
        form = ClassForm()
        form.school_id.choices = [(s.school_id, s.name) for s in School.query.all()]
        if form.validate_on_submit():
            try:
                class_ = Class(
                    school_id=form.school_id.data,
                    name=form.name.data,
                    year=form.year.data
                )
                db.session.add(class_)
                db.session.commit()
                return redirect(url_for("index"))
            except Exception as e:
                print(f"Failed to add class: {e}")
                db.session.rollback()
                form.errors["submit"] = [str(e)]
        return render_template("add_class.html", form=form)

    @app.route("/add_participant", methods=["GET", "POST"])
    def add_participant():
        form = ParticipantForm()
        form.school_id.choices = [(s.school_id, s.name) for s in School.query.all()]
        form.class_id.choices = [(c.class_id, f"{c.name} ({c.school.name})") for c in Class.query.all()]
        if form.validate_on_submit():
            try:
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
                return redirect(url_for("index"))
            except Exception as e:
                print(f"Failed to add participant: {e}")
                db.session.rollback()
                form.errors["submit"] = [str(e)]
        return render_template("add_participant.html", form=form)

    @app.route("/add_sport", methods=["GET", "POST"])
    def add_sport():
        form = SportForm()
        if form.validate_on_submit():
            try:
                sport = Sport(
                    name=form.name.data,
                    description=form.description.data
                )
                db.session.add(sport)
                db.session.commit()
                return redirect(url_for("index"))
            except Exception as e:
                print(f"Failed to add sport: {e}")
                db.session.rollback()
                form.errors["submit"] = [str(e)]
        return render_template("add_sport.html", form=form)

    @app.route("/add_rank", methods=["GET", "POST"])
    def add_rank():
        form = RankForm()
        form.sport_id.choices = [(s.sport_id, s.name) for s in Sport.query.all()]
        if form.validate_on_submit():
            try:
                rank = Rank(
                    sport_id=form.sport_id.data,
                    name=form.name.data,
                    min_points=form.min_points.data
                )
                db.session.add(rank)
                db.session.commit()
                return redirect(url_for("index"))
            except Exception as e:
                print(f"Failed to add rank: {e}")
                db.session.rollback()
                form.errors["submit"] = [str(e)]
        return render_template("add_rank.html", form=form)

    @app.route("/add_participant_rank", methods=["GET", "POST"])
    def add_participant_rank():
        form = ParticipantRankForm()
        form.participant_id.choices = [(p.participant_id, f"{p.first_name} {p.last_name}") for p in
                                       Participant.query.all()]
        form.rank_id.choices = [(r.rank_id, f"{r.name} ({r.sport.name})") for r in Rank.query.all()]
        if form.validate_on_submit():
            try:
                participant_rank = ParticipantRank(
                    participant_id=form.participant_id.data,
                    rank_id=form.rank_id.data,
                    assigned_date=form.assigned_date.data
                )
                db.session.add(participant_rank)
                db.session.commit()
                return redirect(url_for("index"))
            except Exception as e:
                print(f"Failed to add participant rank: {e}")
                db.session.rollback()
                form.errors["submit"] = [str(e)]
        return render_template("add_participant_rank.html", form=form)

    @app.route("/add_event", methods=["GET", "POST"])
    def add_event():
        form = EventForm()
        form.sport_id.choices = [(s.sport_id, s.name) for s in Sport.query.all()]
        form.responsible_id.choices = [(t.teacher_id, f"{t.first_name} {t.last_name}") for t in Teacher.query.all()]
        if form.validate_on_submit():
            try:
                event = Event(
                    sport_id=form.sport_id.data,
                    name=form.name.data,
                    date=form.date.data,
                    location=form.location.data,
                    responsible_id=form.responsible_id.data,
                    distance=form.distance.data
                )
                db.session.add(event)
                db.session.commit()
                return redirect(url_for("index"))
            except Exception as e:
                print(f"Failed to add event: {e}")
                db.session.rollback()
                form.errors["submit"] = [str(e)]
        return render_template("add_event.html", form=form)

    @app.route("/add_teacher", methods=["GET", "POST"])
    def add_teacher():
        form = TeacherForm()
        form.school_id.choices = [(s.school_id, s.name) for s in School.query.all()]
        if form.validate_on_submit():
            try:
                teacher = Teacher(
                    school_id=form.school_id.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    phone=form.phone.data
                )
                db.session.add(teacher)
                db.session.commit()
                return redirect(url_for("index"))
            except Exception as e:
                print(f"Failed to add teacher: {e}")
                db.session.rollback()
                form.errors["submit"] = [str(e)]
        return render_template("add_teacher.html", form=form)

    @app.route("/add_event_participant", methods=["GET", "POST"])
    def add_event_participant():
        form = EventParticipantForm()
        form.event_id.choices = [(e.event_id, f"{e.name} ({e.date})") for e in Event.query.all()]
        form.participant_id.choices = [(p.participant_id, f"{p.first_name} {p.last_name}") for p in
                                       Participant.query.all()]
        if form.validate_on_submit():
            try:
                event_participant = EventParticipant(
                    event_id=form.event_id.data,
                    participant_id=form.participant_id.data,
                    registration_date=form.registration_date.data
                )
                db.session.add(event_participant)
                db.session.commit()
                return redirect(url_for("index"))
            except Exception as e:
                print(f"Failed to add event participant: {e}")
                db.session.rollback()
                form.errors["submit"] = [str(e)]
        return render_template("add_event_participant.html", form=form)

    @app.route("/add_result", methods=["GET", "POST"])
    def add_result():
        form = ResultForm()
        form.event_id.choices = [(e.event_id, f"{e.name} ({e.date})") for e in Event.query.all()]
        form.participant_id.choices = [(p.participant_id, f"{p.first_name} {p.last_name}") for p in
                                       Participant.query.all()]
        form.category_id.choices = [(c.category_id, c.name) for c in Category.query.all()]
        if form.validate_on_submit():
            try:
                # Парсим время (например, "00:01:30" в INTERVAL)
                time_str = form.time.data
                result = Result(
                    event_id=form.event_id.data,
                    participant_id=form.participant_id.data,
                    category_id=form.category_id.data,
                    time=db.session.execute(text(f"SELECT INTERVAL '{time_str}'")).scalar(),
                    points=form.points.data,
                    place=form.place.data
                )
                db.session.add(result)
                db.session.commit()
                return redirect(url_for("index"))
            except Exception as e:
                print(f"Failed to add result: {e}")
                db.session.rollback()
                form.errors["submit"] = [str(e)]
        return render_template("add_result.html", form=form)

    @app.route("/add_school_point", methods=["GET", "POST"])
    def add_school_point():
        form = SchoolPointForm()
        form.school_id.choices = [(s.school_id, s.name) for s in School.query.all()]
        form.event_id.choices = [(e.event_id, f"{e.name} ({e.date})") for e in Event.query.all()]
        if form.validate_on_submit():
            try:
                school_point = SchoolPoint(
                    school_id=form.school_id.data,
                    event_id=form.event_id.data,
                    total_points=form.total_points.data
                )
                db.session.add(school_point)
                db.session.commit()
                return redirect(url_for("index"))
            except Exception as e:
                print(f"Failed to add school point: {e}")
                db.session.rollback()
                form.errors["submit"] = [str(e)]
        return render_template("add_school_point.html", form=form)

    @app.route("/add_category", methods=["GET", "POST"])
    def add_category():
        form = CategoryForm()
        if form.validate_on_submit():
            try:
                category = Category(
                    name=form.name.data,
                    min_age=form.min_age.data,
                    max_age=form.max_age.data,
                    gender=form.gender.data or None
                )
                db.session.add(category)
                db.session.commit()
                return redirect(url_for("index"))
            except Exception as e:
                print(f"Failed to add category: {e}")
                db.session.rollback()
                form.errors["submit"] = [str(e)]
        return render_template("add_category.html", form=form)

    @app.route("/add_log", methods=["GET", "POST"])
    def add_log():
        form = LogForm()
        form.user_id.choices = [(0, "None")] + [(t.teacher_id, f"{t.first_name} {t.last_name}") for t in
                                                Teacher.query.all()]
        if form.validate_on_submit():
            try:
                log = Log(
                    action=form.action.data,
                    user_id=form.user_id.data if form.user_id.data != 0 else None,
                    timestamp=datetime.now()
                )
                db.session.add(log)
                db.session.commit()
                return redirect(url_for("index"))
            except Exception as e:
                print(f"Failed to add log: {e}")
                db.session.rollback()
                form.errors["submit"] = [str(e)]
        return render_template("add_log.html", form=form)