"""
Module contain http routes application
"""
from datetime import datetime

from flask import render_template, request, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.datastructures import FileStorage
from werkzeug.utils import redirect
from app import app, db
from app.models import Account, Mem
from app.service import ImageService, Query
from app.email import send_password_reset_email


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/', methods=['POST', 'GET'])
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


@app.route('/forgot_password', methods=['POST', 'GET'])
def forgot_password():
    if request.form:
        recovered_account = Account.query.filter_by(email=request.form['recovery_email']).first()
        flash(request.form['recovery_email'])
        if not recovered_account:
            return redirect(url_for('forgot_password'))
        send_password_reset_email(recovered_account)
        return render_template('forgot_password/forgot.html', email=request.form['recovery_email'])
    return render_template('forgot_password/forgot.html')

@app.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token: str):
    account: Account = Account.verify_reset_password_token(token)
    if not account:
        return redirect(url_for('index'))
    if request.form:
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if not account:
            return redirect(url_for('index'))
        if not request.form['new_password']:
            flash('Password must contain at least 6 characters')
            return redirect(url_for('reset_password', token=token))
        if not 6 <= len(request.form['new_password']) <= 32:
            flash('The password does not meet the conditions')
            return redirect(url_for('reset_password', token=token))
        form = request.form
        account.set_password(form['new_password'])
        db.session.commit()
        flash('Пароль успешно изменен')
        return redirect(url_for('login'))
    return render_template('forgot_password/reset_password.html')



@app.route('/register', methods=['POST', 'GET'])
def register():
    form = request.form
    # if client send something - checks data
    if len(form) > 0:
        username = form['username']
        email = form['email']
        password = form['password']
        password_repeat = form['password_repeat']
        if password != password_repeat:
            flash('Пароли не совпадают')
            return redirect(url_for('register'))
        user_account = Account(username=username, email=email)
        if Account.query.filter_by(username=user_account.username).first():
            flash('Такой пользователь уже существует')
            return redirect(url_for('register'))
        user_account.set_password(password)
        db.session.add(user_account)
        db.session.commit()
        login_user(user_account)
        flash("Вы успешно вошли!")
        return redirect(url_for('index'))
    return render_template('register/register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = request.form
    # if client send something - checks data
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


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    query = request.args.get('query', default='')
    sort_name = request.args.get('sort', default='')
    service = Query()
    memes = service.get_memes(current_user.id, query, sort_name)
    return render_template('account/account.html', mems=memes, query=query, sort_name=sort_name)


@app.route('/meme/<meme_id>', methods=['GET', 'POST'])
def mem(meme_id):
    image_service = ImageService()
    img = None
    mem = Mem.query.filter_by(id=meme_id).first()
    if mem is not None:
        img = url_for(endpoint='static', filename='/'.join(mem.link.split('/')[1::]))
        print(img)
    if len(request.files) > 0:
        picture: FileStorage = request.files.to_dict()['picture']
        img_name = image_service.save(picture)
        img = url_for('static', filename=f'images/{img_name}')
    print(img)
    mem_tags = ''
    for index, tag in enumerate(mem.tags):
        if index != len(mem.tags) - 1:
            mem_tags += tag.name + ', '
        else:
            mem_tags += tag.name
    mem.view += 1
    db.session.add(mem)
    db.session.commit()
    return render_template('meme/meme.html', img=img, mem=mem, mem_tags=mem_tags)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/redirect")
def add_new_mem(meme_id):
    return redirect(url_for('mem', meme_id=meme_id), 301)


