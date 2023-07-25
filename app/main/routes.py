"""
Module contain http routes application
"""
from datetime import datetime

from flask import render_template, request
from flask_login import current_user

from app import db
from app.main import bp
from app.service import Query


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/', methods=['POST', 'GET'])
@bp.route('/index', methods=['POST', 'GET'])
def index():
    """
    Main page
    """
    # get only public memes
    query = request.args.get('query', default='')
    sort_name = request.args.get('sort', default='')
    service = Query()
    memes = service.get_memes(None, query, sort_name)
    return render_template('public/public.html', mems=memes, query=query, sort_name=sort_name)
