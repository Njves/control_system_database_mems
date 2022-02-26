from flask import render_template

from app import app


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('public/public.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('register/register.html')
