from flask import request, Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()


class Phrase(Resource):
    def get(self):
        return {'name': 'phrase'}

    def post(self):
        args = parser.parse_args()


api.add_resource(Phrase, '/phrase')


if __name__ == '__main__':
    app.run()
