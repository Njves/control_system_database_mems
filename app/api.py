from flask_restful import Resource
from random import randint
from app import api_flask


class Registration(Resource):
    def post(self, username="", email="", password=""):
        return "{\"username\": \"Egor\", \"email\": \"mrpostik@gmail.com\", \"password\": \"123456\"}"


api_flask.add_resource(Registration, "/registration")
