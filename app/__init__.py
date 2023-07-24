import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_babel import Babel

from flask_login import LoginManager
from flask_restful import Api, Resource

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_moment import Moment
from flask_mail import Mail
from flask import request


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
api_flask = Api(app)
mail = Mail(app)
mail.init_app(app)
moment = Moment(app)
babel = Babel(app)
admin_app = Admin(app, name='Memateka', template_mode='bootstrap3')

from app.auth import bp as auth_bp

app.register_blueprint(auth_bp, url_prefix='/auth')

from app.account import bp as account_bp

app.register_blueprint(account_bp)


if not app.debug:
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


from app import models, api, admin, routes

