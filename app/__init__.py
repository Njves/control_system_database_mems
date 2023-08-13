import logging
import os
from logging.handlers import RotatingFileHandler
from logging.handlers import SMTPHandler

from elasticsearch import Elasticsearch
from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please login to access this page'
mail = Mail()
moment = Moment()
admin_app = Admin(name='Memateka', template_mode='bootstrap3')
api_flask = Api()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    api_flask.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    admin_app.init_app(app)
    app.elasticsearch = Elasticsearch([app.config.get('ES_ENDPOINT')]) if app.config.get('ES_ENDPOINT') else None

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.account import bp as account_bp

    app.register_blueprint(account_bp)

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.mem import bp as mem_bp

    app.register_blueprint(mem_bp)

    from app.message import bp as msg_bp

    app.register_blueprint(msg_bp)

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Memateka Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/memateka.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Memateka startup')

    return app

from app import models, api, admin

