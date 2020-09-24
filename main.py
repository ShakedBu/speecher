from flask import request, Flask, Response, json, make_response, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS

from src.group import create_new_group, get_group, search_groups, add_words_to_group, remove_words_from_group
from src.phrase import create_new_phrase, get_phrases
from src.speech import create_new_speech, get_speech, search_speech
from src.word import get_all_words, get_word_by_location, get_word_appearances_in_speech, get_all_words_in_speech
from src.statistics import get_general_counts_by_speech

app = Flask(__name__)
CORS(app)
api = Api(app)
parser = reqparse.RequestParser()


class Word(Resource):
    def get(self):

        if 'speech_id' in request.args:
            if 'paragraph' in request.args:
                return get_word_by_location(request.args['speech_id'], request.args['paragraph'],
                                            request.args['sentence'], request.args['index'])
            elif 'word' in request.args:
                return get_word_appearances_in_speech(request.args['speech_id'], request.args['word'])

            return get_all_words_in_speech(request.args['speech_id'])

        return get_all_words()


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

    def put(self):
        data = request.get_json()
        if data['action'] == 'remove':
            remove_words_from_group(data['id'], data['words'])
        else:
            add_words_to_group(data['id'], data['words'])


class Speech(Resource):
    def get(self):
        if 'id' in request.args:
            return jsonify(get_speech(request.args['id']))

        elif 'query' in request.args:
            return search_speech(request.args['query'])

    def post(self):
        data = request.get_json()
        create_new_speech(data['name'], data['speaker'], data['date'], data['location'], data['file_path'])


# TODO: Return statistics about number of words or characters in sentences etc...
class Statistics(Resource):
    def get(self):
        if 'speech_id' in request.args:
            return get_general_counts_by_speech(get_speech(request.args['speech_id']))


# TODO: Implement the extra subject (XML?)

api.add_resource(Word, '/word')
api.add_resource(Phrase, '/phrase')
api.add_resource(Group, '/group')
api.add_resource(Speech, '/speech')
api.add_resource(Statistics, '/statistics')

if __name__ == '__main__':
    app.run()
