import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    "postgresql: // postgres: 123456 @ localhost:5432 / csdm"
    sqlite = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = sqlite or "postgresql://postgres:123456@localhost:5432/csdm_new"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET-KEY')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = 1
    MAIL_USERNAME = 'mrpostik'
    MAIL_PASSWORD = 'aneamkdcxjnuazpm'
    ADMINS = ['mrpostik@gmail.com']