import werkzeug
from flask import jsonify
from flask_restful import Resource, reqparse
from random import randint
from app import api_flask, db
from app.models import Mem
from app.service import ImageService


class UploadImage(Resource):
    def post(self):
        service = ImageService()
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("tags")
        parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')
        params = parser.parse_args()
        image_file = params['image']
        lnk = service.save(image_file)
        lnk = "static/images/" + lnk
        meme = Mem(name=params['name'], link=lnk, description="Описание", status=0)
        print(params)
        db.session.add(meme)
        db.session.commit()
        return "{\"ok\"}:{\"ok\"}", 201



api_flask.add_resource(UploadImage, "/upload", "/upload/")
