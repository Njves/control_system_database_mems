from flask import render_template

from app import app


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('public/public.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('register/register.html')


@app.route('/account', methods=['POST', 'GET'])
def account():
    return render_template('account/account.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('signIn/signIn.html')


@app.route('/meme/<meme_id>')
def mem(meme_id):
    return render_template('meme/meme.html')



