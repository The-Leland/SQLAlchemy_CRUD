from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

__all__ = ('db', 'init_db')

load_dotenv()

db = SQLAlchemy()

def init_db(app=None):
    if isinstance(app, Flask):

        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
     
        db.init_app(app)

        with app.app_context():
            db.create_all()

    else:
        raise ValueError('cannot init_db without a valid Flask app object')