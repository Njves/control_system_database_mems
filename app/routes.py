"""
Module contain http routes application
"""
import werkzeug.exceptions
from flask import render_template, request, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.datastructures import FileStorage
from werkzeug.utils import redirect

from app import app, db
from app.models import Account, Mem
from app.service import ImageService


@app.route('/', methods=['POST', 'GET'])
def index():
    """
    Main page
    """
    # get only public memes
    memes = Mem.query.filter_by(status=1)
    return render_template('public/public.html', mems=memes)


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
            flash('password is not same')
            return redirect(url_for('register'))
        user_account = Account(username=username, email=email)
        user_account.set_password(password)
        db.session.add(user_account)
        db.session.commit()
        flash("Success!")
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
    memes = Mem.query.filter_by(owner_id=current_user.id).all()
    current_user.amount = len(memes)
    return render_template('account/account.html', mems=memes)


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
    return render_template('meme/meme.html', img=img, mem=mem, mem_tags=mem_tags)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(werkzeug.exceptions.Unauthorized)
def handle_unauthorized_error(e):
    return ":))))", 401


@app.route("/redirect")
def add_new_mem(meme_id):
    return redirect(url_for('mem', meme_id=meme_id), 301)


app.register_error_handler(401, handle_unauthorized_error)
