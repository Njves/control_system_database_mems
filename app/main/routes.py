"""
Module contain http routes application
"""
from datetime import datetime

from flask import render_template, request
from flask_login import current_user

from app import db
from app.main import bp
from app.models import Account, Mem
from app.service import Query


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/', methods=['POST', 'GET'])
def index():
    """
    Main page
    """
    # get only public memes
    query = request.args.get('query', default='')
    sort_name = request.args.get('sort', default='')
    memes = Mem.query.all()
    if query:
        memes, total = Mem.search(query)
        memes = memes.all()

    return render_template('public/public.html', mems=memes, query=query, sort_name=sort_name)
