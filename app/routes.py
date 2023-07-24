"""
Module contain http routes application
"""
from datetime import datetime

from flask import render_template, request, url_for
from flask_login import login_required, current_user
from werkzeug.datastructures import FileStorage
from werkzeug.utils import redirect

from app import app, db
from app.models import Mem
from app.service import ImageService, Query


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

@app.route("/redirect")
def add_new_mem(meme_id):
    return redirect(url_for('mem', meme_id=meme_id), 301)


