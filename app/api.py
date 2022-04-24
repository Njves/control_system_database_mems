"""
The module contains api layer methods
"""
import uuid
from copy import deepcopy, copy

import werkzeug
from flask import jsonify, Response
from flask_restful import Resource, reqparse
from random import randint
from app import api_flask, db
from app.models import Mem, Account
from app.service import ImageService, TagService


class UploadImage(Resource):
    """
    UploadImage designed to create a meme with empty fields,
    but with a link to a picture, also adds a picture to the file system
    Only post
    Request data:
        image: File - mem image,
        owner_id: int - user id
    Response data:
        mem_id: int
    """
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
        account = Account.query.filter_by(uid=params['owner_id']).first()
        print(account)
        account.amount += 1
        meme = Mem(name="", link=lnk, description="", status=0, uid=str(uuid.uuid4()), owner=account)
        db.session.add(meme)
        db.session.add(account)
        db.session.commit()
        data = {"id": meme.id}

        return jsonify(data)


class MemeApi(Resource):
    """
    Api for interacting with meme models
    GET, POST, PUT, DELETE methods
    """
    tag_service = TagService()
    image_service = ImageService()
    def get(self, id):
        """
        Request data:
            id: int - mem id
        Response data:
            mem: str - mem json
        """
        return Mem.query.filter_by(id=id)

    def post(self):
        """
        Request data:
            name: str - mem name,
            link: str - link to mem image,
            description: str - mem description,
            status: int, status visibility mem 0 - private, 1 - public
            owner_id: int - user id
        Response data:
            mem: str - mem json
        """
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('link')
        parser.add_argument('description')
        parser.add_argument('status')
        parser.add_argument('owner_id')
        params = parser.parse_args()

        account = Account.query.filter_by(uid=params['owner_id']).first()
        mem = Mem(name=params['name'], link=params['link'], description=params['description'], likes=0, status=params['status'], owner=account)
        db.session.add(mem)
        db.session.commit()

    def delete(self):
        """
        Request data:
            id: int - id mem,
            owner_id: int, id user
        Response data:
            code: int, 1 - success, 0 - failure
        """
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('owner_id')
        params = parser.parse_args()
        id = params['id']

        account = Account.query.filter_by(uid=params['owner_id']).first()
        if account is None:
            return Response("{}", status=403)
        else:
            if account.uid != params['owner_id']:
                return Response("{}", status=403)

        account.amount -= 1
        mem_query = Mem.query.filter_by(id=id)
        mem = mem_query.first()
        tags = copy(mem.tags)
        print(tags)
        for tag in tags:
            print(tag)
            mem.tags.remove(tag)
            db.session.commit()

        filename = mem.link.split('/')[-1]
        print(filename)
        self.image_service.delete(filename)
        mem_query.delete()
        db.session.add(account)
        db.session.commit()

    def put(self):
        """
        Request data:
            name: str - mem name,
            description: str - mem description,
            status: int, status visibility mem 0 - private, 1 - public
            owner_id: int - user id,
            tags: str, raw string contain tags
        Response data:
            mem: str - mem json
        """

        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('status')
        parser.add_argument('name')
        parser.add_argument('description')
        parser.add_argument('tags')
        parser.add_argument('owner_id')
        params = parser.parse_args()
        print(params)
        requester = Account.query.filter_by(uid=params['owner_id']).first()
        mem = Mem.query.filter_by(id=params['id']).first()
        owner = Account.query.filter_by(id=mem.owner_id).first()
        if requester.uid != owner.uid:
            return 403
        mem.status = int(params['status'] == 'true')
        mem.name = params['name']
        mem.description = params['description']
        mem.tags = self.tag_service.parse_tag(params['tags'])
        db.session.add(mem)
        db.session.commit()


api_flask.add_resource(UploadImage, '/upload', '/upload/')
api_flask.add_resource(MemeApi, '/meme/create', '/meme/delete', '/meme/put')
