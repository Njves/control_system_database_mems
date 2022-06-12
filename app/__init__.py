from flask import Flask

from flask_login import LoginManager
from flask_restful import Api, Resource

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api_flask = Api(app)
admin_app = Admin(app, name='Memateka', template_mode='bootstrap3')


from app import routes, models, api, admin
