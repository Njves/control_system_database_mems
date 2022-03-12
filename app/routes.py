from flask import render_template

from app import app


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('public/public.html')


@app.route('/registration', methods=['POST', 'GET'])
def register():
    return render_template('register/register.html')


@app.route('/detail_mem', methods=['POST', 'GET'])
def detail():
    return render_template('detail_mem/detail_mem.html')
