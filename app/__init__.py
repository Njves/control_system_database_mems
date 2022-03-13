from flask import Flask
from flask_restful import Api, Resource

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api_flask = Api(app)


from app import routes, models, api
