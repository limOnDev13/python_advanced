from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db: SQLAlchemy = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:///prod.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    db.init_app(app)

    return app
