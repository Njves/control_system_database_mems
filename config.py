import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    "postgresql: // postgres: 123456 @ localhost:5432 / csdm"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql://postgres:123456@localhost:5432/csdm_new"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET-KEY')