from typing import List

from flask import render_template
from flask_mail import Message
from app import mail, app
from app.models import Account
from threading import Thread

def send_email(subject: str, sender: str, recipients: List[str] | str, text_body: str, html_body: str):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_password_reset_email(account: Account):
    token = account.get_reset_password_token()
    send_email('[Memateka] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[account.email],
               text_body=render_template('email/reset_password.txt',
                                         account=account, token=token),
               html_body=render_template('email/reset_password.html',
                                         account=account, token=token))