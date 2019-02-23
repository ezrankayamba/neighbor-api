# app/__init__.py
from flask import Flask, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_migrate import Migrate
import os
import collections
from config import app_config

db = SQLAlchemy()
admin = Admin(name='Neighbor APIs', template_mode='bootstrap3')


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config['dev'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True

    db.init_app(app)

    # Flask admin
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin.init_app(app)

    migrate = Migrate(app, db)
    from app import models, utils

    from .neighbors import neighbors as neighbors_blueprint
    app.register_blueprint(neighbors_blueprint, url_prefix='/neighbors')
    from .groups import groups as groups_blueprint
    app.register_blueprint(groups_blueprint, url_prefix='/groups')

    return app
