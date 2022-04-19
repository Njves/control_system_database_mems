import uuid

import werkzeug
from flask import jsonify
from flask_restful import Resource, reqparse
from random import randint
from app import api_flask, db
from app.models import Mem, Account
from app.service import ImageService


class UploadImage(Resource):
    def post(self):
        service = ImageService()
        parser = reqparse.RequestParser()
        parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('owner_id')
        params = parser.parse_args()
        image_file = params['image']
        filename = service.save(image_file)
        lnk = ImageService.IMG_PATH + filename
        print(params)
        account = Account.query.filter_by(id=params['owner_id']).first()
        print(account)
        account.amount += 1
        meme = Mem(name="", link=lnk, description="", status=0, uid=str(uuid.uuid4()), owner=account)
        db.session.add(meme)
        db.session.add(account)
        db.session.commit()
        data = {"id": meme.id}

        return jsonify(data)


class MemeApi(Resource):
    def get(self, id):
        return Mem.query.filter_by(id=id)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('link')
        parser.add_argument('description')
        parser.add_argument('status')
        parser.add_argument('owner_id')
        params = parser.parse_args()

        account = Account.query.filter_by(id=params['owner_id'])
        mem = Mem(name=params['name'], link=params['link'], description=params['description'], likes=0, status=params['likes'], owner=account)
        db.session.add(mem)
        db.session.commit()

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        params = parser.parse_args()
        id = params['id']
        Mem.query.filter_by(id=id).delete()
        db.session.commit()

    def get_method(self):
        parser = reqparse.RequestParser()
        parser.add_argument('_method')
        data = parser.parse_args()
        return data['_method']

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('status')
        params = parser.parse_args()
        print(params)
        mem = Mem.query.filter_by(id=params['id']).first()
        mem.status = int(params['status'] == 'true')
        db.session.add(mem)
        db.session.commit()


api_flask.add_resource(UploadImage, '/upload', '/upload/')
api_flask.add_resource(MemeApi, '/meme/create', '/meme/delete', '/meme/put')
