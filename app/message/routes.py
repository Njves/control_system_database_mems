from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.message import bp
from app.models import Account, Message


@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    account = Account.query.filter_by(username=recipient).first_or_404()
    form = request.form
    if form:
        if not form['text']:
            return render_template('message/send_message.html')
        message = Message(author=current_user, recipient=account, body=form['text'])
        db.session.add(message)
        db.session.commit()
    return render_template('message/send_message.html', messages=Message.query.all())


@bp.route('/messages/', methods=['GET'])
@login_required
def messages():
    accounts = Account.query.all()
    accounts.remove(current_user)
    return render_template('message/messages.html', accounts=accounts)