# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, FloatField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange

class SchoolForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    address = StringField("Address", validators=[Optional()])
    contact_phone = StringField("Contact Phone", validators=[Optional()])
    submit = SubmitField("Add School")

class ClassForm(FlaskForm):
    school_id = SelectField("School", coerce=int, validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    year = IntegerField("Year", validators=[Optional(), NumberRange(min=1900, max=2100)])
    submit = SubmitField("Add Class")

class ParticipantForm(FlaskForm):
    school_id = SelectField("School", coerce=int, validators=[DataRequired()])
    class_id = SelectField("Class", coerce=int, validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    birth_date = DateField("Birth Date", validators=[DataRequired()])
    gender = SelectField("Gender", choices=[("M", "Male"), ("F", "Female")], validators=[DataRequired()])
    submit = SubmitField("Add Participant")

class SportForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    submit = SubmitField("Add Sport")

class RankForm(FlaskForm):
    sport_id = SelectField("Sport", coerce=int, validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    min_points = IntegerField("Min Points", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Add Rank")

class ParticipantRankForm(FlaskForm):
    participant_id = SelectField("Participant", coerce=int, validators=[DataRequired()])
    rank_id = SelectField("Rank", coerce=int, validators=[DataRequired()])
    assigned_date = DateField("Assigned Date", validators=[DataRequired()])
    submit = SubmitField("Add Participant Rank")

class EventForm(FlaskForm):
    sport_id = SelectField("Sport", coerce=int, validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    location = StringField("Location", validators=[Optional()])
    responsible_id = SelectField("Responsible Teacher", coerce=int, validators=[DataRequired()])
    distance = FloatField("Distance", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Add Event")

class TeacherForm(FlaskForm):
    school_id = SelectField("School", coerce=int, validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    phone = StringField("Phone", validators=[Optional()])
    submit = SubmitField("Add Teacher")

class EventParticipantForm(FlaskForm):
    event_id = SelectField("Event", coerce=int, validators=[DataRequired()])
    participant_id = SelectField("Participant", coerce=int, validators=[DataRequired()])
    registration_date = DateField("Registration Date", validators=[DataRequired()])
    submit = SubmitField("Add Event Participant")

class ResultForm(FlaskForm):
    event_id = SelectField("Event", coerce=int, validators=[DataRequired()])
    participant_id = SelectField("Participant", coerce=int, validators=[DataRequired()])
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    time = StringField("Time (e.g., 00:01:30)", validators=[DataRequired()])
    points = IntegerField("Points", validators=[DataRequired(), NumberRange(min=0)])
    place = IntegerField("Place", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Add Result")

class SchoolPointForm(FlaskForm):
    school_id = SelectField("School", coerce=int, validators=[DataRequired()])
    event_id = SelectField("Event", coerce=int, validators=[DataRequired()])
    total_points = IntegerField("Total Points", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Add School Point")

class CategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    min_age = IntegerField("Min Age", validators=[DataRequired(), NumberRange(min=0)])
    max_age = IntegerField("Max Age", validators=[DataRequired(), NumberRange(min=0)])
    gender = SelectField("Gender", choices=[("", "Any"), ("M", "Male"), ("F", "Female")], validators=[Optional()])
    submit = SubmitField("Add Category")

class LogForm(FlaskForm):
    action = StringField("Action", validators=[DataRequired()])
    user_id = SelectField("User (Teacher)", coerce=int, validators=[Optional()])
    submit = SubmitField("Add Log")