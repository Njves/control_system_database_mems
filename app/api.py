import werkzeug
from flask import jsonify
from flask_restful import Resource, reqparse
from random import randint
from app import api_flask
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
        service.save(image_file)
        print(params)
        return "{}:{}", 201



api_flask.add_resource(UploadImage, "/upload", "/upload/")
