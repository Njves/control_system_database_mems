from flask_restful import Resource
from random import randint
from app import api_flask


class MyRegister(Resource):
    def get(self, id=0):
        return randint(1, 10) + (id * 100), 200

api_flask.add_resource(MyRegister, "/register", "/register/<int:id>")
