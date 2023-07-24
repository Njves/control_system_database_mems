import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    sqlite = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = sqlite if os.environ.get('FLASK_DEBUG') else os.environ.get('DB_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET-KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = 1
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['mrpostik@gmail.com']