from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

rstdb = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(config[config_name]())
    rstdb.init_app(app)
    rstdb.app = app

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from .kitchen import kitchen as kitchen_blueprint
    app.register_blueprint(kitchen_blueprint, url_prefix='/kitchen')

    return app
