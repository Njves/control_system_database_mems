from flask import Blueprint

bp = Blueprint('message', __name__)

from app.message import routes