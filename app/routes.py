import os

from flask import render_template, request, url_for, flash
from flask_login import login_user
from werkzeug.datastructures import FileStorage
from werkzeug.utils import redirect

import config
from app import app, db
from app.forms import LoginForm
from app.models import Account, Mem
from app.service import ImageService


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('public/public.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = request.form
    if len(form) > 0:
        username = form['username']
        email = form['email']
        password = form['password']
        password_repeat = form['password_repeat']
        if password != password_repeat:
            flash('password is not same')
            return redirect(url_for('register'))
        user_account = Account(username=username, email=email)
        user_account.set_password(password)
        db.session.add(user_account)
        db.session.commit()
        flash("Success!")
        return redirect(url_for('index'))
    return render_template('register/register.html')


@app.route('/account', methods=['POST', 'GET'])
def account():
    print(request.files)
    mem_list = Mem.query.all()
    return render_template('account/account.html', mem_list)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = request.form
    if len(form) > 0:
        username_or_email = form['username_email']
        password = form['password']
        user_account: Account = Account.query.filter_by(username=username_or_email).first()
        if user_account is None or not user_account.check_password(password):
            flash('Invalid username or password')
            return redirect("/login")
        login_user(user_account)
        flash("Success!")
        return redirect(url_for('index'))
    return render_template('signIn/signIn.html')


@app.route('/meme/<meme_id>', methods=['GET', 'POST'])
def mem(meme_id):
    image_service = ImageService()
    print(request.form.to_dict())
    print(request.files.to_dict())
    img = None
    if len(request.files) > 0:
        picture: FileStorage = request.files.to_dict()['picture']
        img_name = image_service.save(picture)
        img = url_for('static', filename=f'images/{img_name}')
    return render_template('meme/meme.html', img=img)



