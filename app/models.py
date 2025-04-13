# app/models.py
from . import db
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy import UniqueConstraint


class School(db.Model):
    __tablename__ = "schools"

    school_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(200))
    contact_phone = db.Column(db.String(20))

    def __repr__(self):
        return f"<School {self.name}>"


class Class(db.Model):
    __tablename__ = "classes"

    class_id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.school_id", ondelete="RESTRICT"), nullable=False)
    name = db.Column(db.String(10), nullable=False)
    year = db.Column(db.Integer)

    __table_args__ = (UniqueConstraint("school_id", "name", name="uix_school_name"),)

    def __repr__(self):
        return f"<Class {self.name}>"


class Participant(db.Model):
    __tablename__ = "participants"

    participant_id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.school_id", ondelete="RESTRICT"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.class_id", ondelete="RESTRICT"), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(1), nullable=False)

    def __repr__(self):
        return f"<Participant {self.first_name} {self.last_name}>"


class Sport(db.Model):
    __tablename__ = "sports"

    sport_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<Sport {self.name}>"


class Rank(db.Model):
    __tablename__ = "ranks"

    rank_id = db.Column(db.Integer, primary_key=True)
    sport_id = db.Column(db.Integer, db.ForeignKey("sports.sport_id", ondelete="RESTRICT"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    min_points = db.Column(db.Integer, nullable=False)

    __table_args__ = (UniqueConstraint("sport_id", "name", name="uix_sport_name"),)

    def __repr__(self):
        return f"<Rank {self.name}>"


class ParticipantRank(db.Model):
    __tablename__ = "participant_ranks"

    participant_id = db.Column(db.Integer, db.ForeignKey("participants.participant_id", ondelete="CASCADE"),
                               primary_key=True)
    rank_id = db.Column(db.Integer, db.ForeignKey("ranks.rank_id", ondelete="CASCADE"), primary_key=True)
    assigned_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<ParticipantRank participant_id={self.participant_id}>"


class Event(db.Model):
    __tablename__ = "events"

    event_id = db.Column(db.Integer, primary_key=True)
    sport_id = db.Column(db.Integer, db.ForeignKey("sports.sport_id", ondelete="RESTRICT"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(200))
    responsible_id = db.Column(db.Integer, db.ForeignKey("teachers.teacher_id", ondelete="RESTRICT"), nullable=False)
    distance = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Event {self.name}>"


class Teacher(db.Model):
    __tablename__ = "teachers"

    teacher_id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.school_id", ondelete="RESTRICT"), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))

    def __repr__(self):
        return f"<Teacher {self.first_name} {self.last_name}>"


class EventParticipant(db.Model):
    __tablename__ = "event_participants"

    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id", ondelete="CASCADE"), primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.participant_id", ondelete="CASCADE"),
                               primary_key=True)
    registration_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<EventParticipant event_id={self.event_id}>"


class Result(db.Model):
    __tablename__ = "results"

    result_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id", ondelete="RESTRICT"), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.participant_id", ondelete="RESTRICT"),
                               nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id", ondelete="RESTRICT"), nullable=False)
    time = db.Column(INTERVAL, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    place = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Result result_id={self.result_id}>"


class SchoolPoint(db.Model):
    __tablename__ = "school_points"

    school_id = db.Column(db.Integer, db.ForeignKey("schools.school_id", ondelete="CASCADE"), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id", ondelete="CASCADE"), primary_key=True)
    total_points = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<SchoolPoint school_id={self.school_id}>"


class Category(db.Model):
    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    min_age = db.Column(db.Integer, nullable=False)
    max_age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(1))

    def __repr__(self):
        return f"<Category {self.name}>"


class Log(db.Model):
    __tablename__ = "logs"

    log_id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("teachers.teacher_id", ondelete="SET NULL"))
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def __repr__(self):
        return f"<Log {self.action}>"