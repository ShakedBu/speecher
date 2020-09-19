from flask import request, Flask, Response, json, make_response
from flask_restful import reqparse, abort, Api, Resource

from src.group import create_new_group, get_group, search_groups
from src.phrase import create_new_phrase, get_phrases
from src.speech import create_new_speech, get_speech, search_speech

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()


class Word(Resource):
    def get(self):
        # TODO: Get all of the words by speech
        # TODO: Get word by location!
        return ''


class Phrase(Resource):
    def get(self):
        return get_phrases(request.args['speech_id'], request.args['query'])

    def post(self):
        data = request.get_json()
        create_new_phrase(data['words'])


class Group(Resource):
    def get(self):
        if 'id' in request.args:
            return get_group(request.args['id'])

        elif 'query' in request.args:
            return search_groups(request.args['query'])

    def post(self):
        data = request.get_json()
        create_new_group(data['name'], data['words'])


class Speech(Resource):
    def get(self):
        if 'id' in request.args:
            return get_speech(request.args['id'])

        elif 'query' in request.args:
            result = search_speech(request.args['query'])
            resp = Response(json.dumps(result), status=200, mimetype='application/json')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp

    def post(self):
        data = request.get_json()
        create_new_speech(data['name'], data['speaker'], data['date'], data['location'], data['file_path'])


# TODO: Return statistics about number of words or characters in sentences etc...
# TODO: Implement the extra subject (XML?)

api.add_resource(Word, '/word')
api.add_resource(Phrase, '/phrase')
api.add_resource(Group, '/group')
api.add_resource(Speech, '/speech')


if __name__ == '__main__':
    app.run()
