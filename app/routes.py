# app/routes.py
from flask import render_template
from .models import School

def register_routes(app):
    @app.route("/")
    def index():
        schools = School.query.all()
        return render_template("index.html", schools=schools)