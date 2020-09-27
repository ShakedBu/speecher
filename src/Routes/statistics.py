from flask_restful import Resource
from flask import request

from src.DBUtils import execute_query
from src.queries import GET_ALL_COUNTS


class Statistics(Resource):
    def get(self):
        if 'speech_id' in request.args:
            if 'count' in request.args:
                if request.args['count'] == 'char':
                    return count_chars(request.args['speech_id'], request.args.get('paragraph'),
                                       request.args.get('sentence'), request.args.get('word'))
                return count_words(request.args['speech_id'], request.args.get('paragraph'),
                                   request.args.get('sentence'))
        return get_general_counts_by_speech(request.args['speech_id'])


def get_general_counts_by_speech(speech_id):
    results = []
    counts = execute_query(GET_ALL_COUNTS.format(speech_id), True)
    paragraph_index = 1
    paragraph_sentences = []

    for count in counts:
        if count[0] == paragraph_index:
            paragraph_sentences.append({'sentence': count[1], 'words': count[2]})
        else:
            results.append({'paragraph': paragraph_index, 'sentences': paragraph_sentences})
            paragraph_index += 1
            paragraph_sentences = [{'sentence': count[1], 'words': count[2]}]

    results.append({'paragraph': paragraph_index, 'sentences': paragraph_sentences})

    return results


def count_words(speech_id, paragraph, sentence):
    return 0


def count_chars(speech_id, paragraph, sentence, word):
    return 0


def count_words_appearances(speech_id):
    return 0
