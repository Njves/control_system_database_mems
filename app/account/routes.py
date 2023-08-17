from flask import render_template, request
from flask_login import login_required

from app.account import bp
from app.models import Mem


@bp.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    query = request.args.get('query', default='')
    sort_name = request.args.get('sort', default='')
    if query:
        memes, total = Mem.search(query)
        memes = memes.all()
    return render_template('account/account.html', mems=memes, query=query, sort_name=sort_name)