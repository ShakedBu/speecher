from flask import request, Flask
from flask_restful import reqparse, abort, Api, Resource

from src.speech import create_new_speech, get_speech

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()


class Phrase(Resource):
    def get(self):
        return {'name': 'phrase'}

    def post(self):
        args = parser.parse_args()


class Group(Resource):
    def get(self):
        return {'name': 'Group'}

    def post(self):
        args = parser.parse_args()


class Speech(Resource):
    def get(self):
        return get_speech(request.args['id'])

    def post(self):
        data = request.get_json()
        create_new_speech(data['name'], data['speaker'], data['date'], data['location'], data['file_path'])


api.add_resource(Phrase, '/phrase')
api.add_resource(Group, '/group')
api.add_resource(Speech, '/speech')


if __name__ == '__main__':
    app.run()
