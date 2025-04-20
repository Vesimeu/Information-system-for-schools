# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, FloatField, SelectField, TextAreaField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Optional, NumberRange, Length, Regexp, ValidationError
from datetime import datetime

class SchoolForm(FlaskForm):
    name = StringField('Название школы', validators=[DataRequired(), Length(min=2, max=100)])
    address = StringField('Адрес', validators=[DataRequired(), Length(min=5, max=200)])
    contact_phone = StringField('Контактный телефон', validators=[DataRequired(), Length(min=5, max=20)])
    submit = SubmitField('Добавить школу')


class ClassForm(FlaskForm):
    school_id = SelectField('Школа', coerce=int, validators=[DataRequired()])
    name = StringField('Название класса', validators=[DataRequired()])
    year = IntegerField('Год', validators=[DataRequired()])
    teacher_id = SelectField('Классный руководитель', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Добавить')

class ParticipantForm(FlaskForm):
    school_id = SelectField('Школа', coerce=int, validators=[DataRequired()])
    class_id = SelectField('Класс', coerce=int, validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(min=2, max=50)])
    birth_date = DateField('Дата рождения', validators=[DataRequired()])
    gender = SelectField('Пол', choices=[('M', 'Мужской'), ('F', 'Женский')], validators=[DataRequired()])
    submit = SubmitField('Добавить участника')

class SportForm(FlaskForm):
    name = StringField('Название вида спорта', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Описание', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Добавить вид спорта')

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
    school_id = SelectField('Школа', coerce=int, validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Фамилия', validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField('Телефон', validators=[DataRequired(), Length(min=5, max=20)])
    submit = SubmitField('Добавить учителя')

class EventParticipantForm(FlaskForm):
    event_id = SelectField("Event", coerce=int, validators=[DataRequired()])
    participant_id = SelectField("Participant", coerce=int, validators=[DataRequired()])
    registration_date = DateField("Registration Date", validators=[DataRequired()])
    submit = SubmitField("Add Event Participant")

class ResultForm(FlaskForm):
    time = StringField('Время (ЧЧ:ММ:СС)', validators=[DataRequired()])
    points = IntegerField('Очки', validators=[DataRequired()])
    place = IntegerField('Место', validators=[DataRequired()])
    category_id = SelectField('Категория', coerce=int, validators=[DataRequired()])

    def validate_time(self, field):
        try:
            h, m, s = map(int, field.data.split(':'))
            if not (0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59):
                raise ValidationError('Некорректный формат времени')
        except:
            raise ValidationError('Время должно быть в формате ЧЧ:ММ:СС')

class SchoolPointForm(FlaskForm):
    school_id = SelectField("School", coerce=int, validators=[DataRequired()])
    event_id = SelectField("Event", coerce=int, validators=[DataRequired()])
    total_points = IntegerField("Total Points", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Add School Point")

class CategoryForm(FlaskForm):
    name = StringField('Название категории', validators=[DataRequired()])
    min_age = IntegerField('Минимальный возраст', validators=[DataRequired()])
    max_age = IntegerField('Максимальный возраст', validators=[DataRequired()])
    gender = SelectField('Пол', choices=[('', 'Любой'), ('М', 'Мужской'), ('Ж', 'Женский')])
    submit = SubmitField('Добавить')

class LogForm(FlaskForm):
    action = StringField("Action", validators=[DataRequired()])
    user_id = SelectField("User (Teacher)", coerce=int, validators=[Optional()])
    submit = SubmitField("Add Log")

class EventCreationForm(FlaskForm):
    name = StringField('Название мероприятия', validators=[DataRequired(), Length(min=2, max=200)])
    date = DateField('Дата проведения', validators=[DataRequired()])
    location = StringField('Место проведения', validators=[DataRequired(), Length(min=2, max=200)])
    sport_id = SelectField('Вид спорта', coerce=int, validators=[DataRequired()])
    responsible_id = SelectField('Ответственный', coerce=int, validators=[DataRequired()])
    distance = StringField('Дистанция', validators=[Optional(), Length(max=50)])
    participants = SelectMultipleField('Участники', coerce=int, validators=[DataRequired()])
    categories = SelectMultipleField('Категории', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Создать мероприятие')