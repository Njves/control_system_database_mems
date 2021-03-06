"""
Module contain http routes application
"""
import werkzeug.exceptions
from flask import render_template, request, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import desc, asc
from werkzeug.datastructures import FileStorage
from werkzeug.utils import redirect

from app import app, db
from app.models import Account, Mem, Tag
from app.service import ImageService


@app.route('/', methods=['POST', 'GET'])
def index():
    """
    Main page
    """
    # get only public memes
    query = request.args.get('query', default='')
    sort_name = request.args.get('sort', default='')
    memes_query = Mem.query.filter_by(status=1)
    all_memes = memes_query.all()
    print("all_memes", all_memes)

    sort_various = {'by_title': memes_query.order_by(asc(Mem.name)),
                    'by_likes': memes_query.order_by(desc(Mem.likes)),
                    'by_view': memes_query.order_by(desc(Mem.view))}
    found_tagged_mem = []
    if query:
        memes_query = memes_query.filter(Mem.name.like("%" + query + "%"))
        for current_mem in all_memes:
            for tag in current_mem.tags:
                print(tag, tag.name.startswith(query))
                if tag.name.startswith(query):
                    found_tagged_mem.append(current_mem)


    if sort_name:
        memes_query = sort_various.get(sort_name, '')
    memes = memes_query.all()
    for i in found_tagged_mem:
        if i not in memes:
            memes.append(i)
    print(memes)
    return render_template('public/public.html', mems=memes, query=query, sort_name=sort_name)


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
        user_account.set_password(password)
        db.session.add(user_account)
        db.session.commit()
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
    memes_query = Mem.query.filter_by(owner_id=current_user.id)
    all_memes = memes_query.all()
    sort_various = {'by_title': memes_query.order_by(asc(Mem.name)),
                    'by_likes': memes_query.order_by(desc(Mem.likes)),
                    'by_view': memes_query.order_by(desc(Mem.view))}
    found_tagged_mem = []
    if query:
        memes_query = memes_query.filter(Mem.name.like("%" + query + "%"))
        for current_mem in all_memes:
            for tag in current_mem.tags:
                print(tag, tag.name.startswith(query))
                if tag.name.startswith(query):
                    found_tagged_mem.append(current_mem)

    if sort_name:
        memes_query = sort_various.get(sort_name, '')
    memes = memes_query.all()
    for i in found_tagged_mem:
        if i not in memes:
            memes.append(i)
    print(memes)
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


