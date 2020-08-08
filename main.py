from flask import request, Flask
from flask_restful import reqparse, abort, Api, Resource

from src.DBUtils import call_db

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()


class Phrase(Resource):
    def get(self):
        return {'name': 'phrase'}

    def post(self):
        args = parser.parse_args()


class Speech(Resource):
    def get(self):
        call_db()
        return {'name': 'speech'}

    def post(self):
        args = parser.parse_args()


api.add_resource(Phrase, '/phrase')
api.add_resource(Speech, '/speech')


if __name__ == '__main__':
    app.run()
