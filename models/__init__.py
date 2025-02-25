from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()  # Initialize without app

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)  # Bind db to app
    return app