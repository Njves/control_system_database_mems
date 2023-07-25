from flask import Blueprint

bp = Blueprint('mem', __name__)

from app.mem import routes