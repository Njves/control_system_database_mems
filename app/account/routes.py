from flask import render_template, request
from flask_login import login_required, current_user

from app.account import bp
from app.service import Query


@bp.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    query = request.args.get('query', default='')
    sort_name = request.args.get('sort', default='')
    service = Query()
    memes = service.get_memes(current_user.id, query, sort_name)
    return render_template('account/account.html', mems=memes, query=query, sort_name=sort_name)