from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import app_config

db = SQLAlchemy()
def create_app(config_name):
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_object(app_config[config_name])
    application.config.from_pyfile('config.py')
    db.init_app(application)
    Migrate(application, db)

    from app.scrapper import models

    from app.scrapper.controllers import main
    application.register_blueprint(main, url_prefix='/')

    return application