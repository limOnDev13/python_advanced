from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db: SQLAlchemy = SQLAlchemy()

from .app import create_app


def db_create_all(app_: Flask):
    with app_.app_context():
        db.create_all()
